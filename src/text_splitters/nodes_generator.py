from .chunks_generator import ChunksGeneratorInterface
from utils import Domain
from knowledge_graph import KGBuilder
from infrastructure import Neo4jConnection
from knowledge_graph import OntologyAnalyzer
from utils import set_graph


class NodesGenerator(ChunksGeneratorInterface):
  def __init__(self, 
               document_name: str, 
               ontology_name: str, 
               model_name: str,
               neo4j_connection: Neo4jConnection,
               domain: Domain,
               mitigation_only:bool = False):
    self.document_name = document_name
    self.ontology_name = ontology_name
    self.model_name = model_name
    self.neo4j_connection = neo4j_connection
    self.domain = domain
    self.mitigation_only = mitigation_only


  def get_nodes(self) -> list[str]:
    pass

  
  def _load_document(self) -> str:
    with open(self.document_name, 'r', encoding='utf-8') as file:
      return file.read().replace('\n', ' ')
    
    
  def _get_ontology(self) -> str:
    onto_analyzer = OntologyAnalyzer(f"ontologies/{self.ontology_name}.ttl")
    return onto_analyzer.get_ontology_summary()
  

  def _build_knowledge_graph(self, ontology: str, document: str) -> str:
    self.kg_builder = KGBuilder(model_name=self.model_name, temperature=0, domain=self.domain, ontology=ontology, document=document)
    graph = self.kg_builder.build_kg()
    return graph
  

  def _store_in_neo4j(self, graph: str):
    try:
      self.neo4j_connection.store_graph(graph, self.domain)
      return True
    except Exception as e:
      print(f"Error storing data in Neo4j: {e}")
      return False
    

  def _store_results_in_txt(self, triples: str, model_name: str):
    file_name = self.document_name.split('\\')[-1].split('.')[0]
    print(f"\nStoring results in 'graphs/{file_name}_{model_name}.ttl'...")
    with open(f"../graphs/{file_name}_{model_name.replace(':', '_')}.ttl", 'a', encoding='utf-8') as f:
      f.write(triples)
    

  def get_chunks(self) -> list[str]:
    document = self._load_document()
    ontology = self._get_ontology()
    if not self.mitigation_only:
      print("Building knowledge graph...")
      graph = self._build_knowledge_graph(ontology, document)
      print("Knowledge graph built. Storing in Neo4j...")
      if self._store_in_neo4j(graph):
        print("Data stored in Neo4j.")
      else:
        print("Failed to store data in Neo4j. Attempting to validate and fix the graph...")
        fixed_graph = self.kg_builder.validate_graph(graph, ontology)
        self._store_in_neo4j(fixed_graph)
        return []
      self._store_results_in_txt(graph, self.model_name)
    else: # Get data from Neo4j
      set_graph(self.document_name, self.domain, self.neo4j_connection)
    labels = self.neo4j_connection.load_triples_from_neo4j()
    return labels