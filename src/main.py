from bias_mitigation import LegalBiasMitigator, JobPostingBiasMitigator
from bias_mitigation import CustomRAG
from bias_detection import EmbeddingsGenderBiasDetector   
from bias_mitigation import EntitiesExtractor
from utils import Domain
from infrastructure import Neo4jConnection
from bias_detection import LexicographicalBiasDetector
from text_splitters import SentencesGenerator
from text_splitters import NodesGenerator
from infrastructure import SqlLiteConnection
from bias_detection import LegalBiasDetectorService, JobPostingBiasDetectorService 
import yaml
from dotenv import load_dotenv
import json
import os


if __name__ == "__main__":
  # Resolve project root relative to this script (src/../ = project root)
  PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

  # Load environment variables from the correct location
  env_path = os.path.join(PROJECT_ROOT, 'data', 'config', '.env')
  load_dotenv(env_path)
  
  neo4j_uri = os.getenv("NEO4J_URI")
  neo4j_user = os.getenv("NEO4J_USERNAME")
  neo4j_password = os.getenv("NEO4J_PASSWORD")

  # Verify environment variables are loaded
  if not neo4j_uri or not neo4j_user or not neo4j_password:
    raise ValueError("Neo4j credentials not found in .env file. Please check data/config/.env")

  with open(os.path.join(PROJECT_ROOT, 'data', 'config', 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

  GRAPH_CONSTRUCTION_MODEL = config['model']['slm']['graph_construction']
  MITIGATION_MODEL = config['model']['slm']['mitigation']
  TEMPERATURE = config['model']['slm']['temperature']
  EMBEDDINGS_MODEL = config['model']['embeddings']['name']
  NLP_MODEL = config['model']['embeddings']['nlp_model']
  def resolve(path):
    return os.path.join(PROJECT_ROOT, path.lstrip('./\\'))

  SQL_PATH = resolve(config['database']['sqlite_path'])
  THRESHOLD = config['thresholds']['bias_threshold']
  WORD_THRESHOLD = config['thresholds']['word_threshold']
  DOMAIN = config['experiment']['domain']
  ONTOLOGY_NAME = config['experiment']['ontology_name']
  GRAPH = resolve(config['experiment']['graph_path'])
  DOCUMENT = resolve(config['experiment']['document_path'])
  RAG_DATA = resolve(config['experiment']['rag_data'])
  MITIGATION_ONLY = config['experiment']['mitigation_only']
  WORD_EMBEDDINGS_FILE = resolve(config['experiment']['embeddings_words_path'])
  EMBEDDINGS_METHOD = config['experiment']['embeddings_method']

  with open(WORD_EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
    words_data = json.load(f)

  with open(RAG_DATA, "r", encoding="utf-8") as f:
    dataset = json.load(f)

  neo4j = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)
  db = SqlLiteConnection(SQL_PATH)
  rag = CustomRAG(dataset)


  male_terms = words_data['male_terms'] 
  female_terms = words_data['female_terms'] 
  
  # TODO: Refactor for something better
  if Domain(DOMAIN) == Domain.LEGAL:
    bias_mitigator = LegalBiasMitigator(model_name=MITIGATION_MODEL, temperature=TEMPERATURE,  rag=rag)
  else:
    bias_mitigator = JobPostingBiasMitigator(model_name=MITIGATION_MODEL, temperature=TEMPERATURE,  rag=rag)
  
  bias_detector = EmbeddingsGenderBiasDetector(male_terms=male_terms, female_terms=female_terms, method=EMBEDDINGS_METHOD)
  semantic_analysis = LexicographicalBiasDetector(db_connector=db, bias_threshold=0)
  chunks_generator = SentencesGenerator(document_name=DOCUMENT)
  nodes_generator = NodesGenerator(document_name=GRAPH if MITIGATION_ONLY else DOCUMENT,
                                   ontology_name=ONTOLOGY_NAME, 
                                   model_name=GRAPH_CONSTRUCTION_MODEL, 
                                   neo4j_connection=neo4j,
                                   domain=Domain(DOMAIN), 
                                   mitigation_only=MITIGATION_ONLY)
  entities_extractor = EntitiesExtractor(neo4j_connection=neo4j, db_connection=db)

  if Domain(DOMAIN) == Domain.JOB_POSTING:
    service = JobPostingBiasDetectorService(document_path=DOCUMENT,
                                        bias_mitigator=bias_mitigator,
                                        db_connector=db,
                                        nodes_generator=nodes_generator,
                                        embeddings_bias_detector=bias_detector,
                                        lexicographical_bias_detector=semantic_analysis,
                                        model_name=GRAPH_CONSTRUCTION_MODEL,
                                        mitigation_model_name=MITIGATION_MODEL,
                                        threshold=THRESHOLD, 
                                        word_threshold=WORD_THRESHOLD)
  else:
    service = LegalBiasDetectorService(document_path=DOCUMENT,
                                        bias_mitigator=bias_mitigator,
                                        chunks_generator=chunks_generator,
                                        nodes_generator=nodes_generator,
                                        entities_extractor=entities_extractor,
                                        embeddings_bias_detector=bias_detector, 
                                        lexicographical_bias_detector=semantic_analysis, 
                                        model_name=GRAPH_CONSTRUCTION_MODEL,
                                        mitigation_model_name=MITIGATION_MODEL,
                                        threshold=THRESHOLD, 
                                        word_threshold=WORD_THRESHOLD)

  service.run()
