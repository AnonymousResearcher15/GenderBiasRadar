from data.chunks_generator import ChunksGeneratorInterface
from utils import Domain
from ..knowledge_graph.kg_builder import KGBuilder
from infrastructure.neo4jconnector import Neo4jConnection
from ..knowledge_graph.ontology_analyzer import OntologyAnalyzer
from utils import set_graph


class NodesGenerator(ChunksGeneratorInterface):
  def __init__(self, 
               document_name: str, 
               ontology_name: str, 
               model_name: str,
               neo4j_connection: Neo4jConnection,
               domain: Domain,
               validation_only:bool = False):
    self.document_name = document_name
    self.ontology_name = ontology_name
    self.model_name = model_name
    self.neo4j_connection = neo4j_connection
    self.domain = domain
    self.validation_only = validation_only


  def get_nodes(self) -> list[str]:
    pass

  
  def _load_document(self) -> str:
    with open(self.document_name, 'r', encoding='utf-8') as file:
      return file.read().replace('\n', ' ')
    
    
  def _get_ontology(self) -> str:
    onto_analyzer = OntologyAnalyzer(f"../ontologies/{self.ontology_name}.ttl")
    return onto_analyzer.get_ontology_summary()
  

  def _build_knowledge_graph(self, ontology: str, document: str) -> str:
    kg_builder = KGBuilder(model_name=self.model_name, temperature=0, domain=self.domain, ontology=ontology, document=document)
    graph = kg_builder.build_kg()
    return graph
  

  def _store_in_neo4j(self, graph: str):
    self.neo4j_connection.store_graph(graph, self.domain)
    
  def get_chunks(self) -> list[str]:
    document = self._load_document()
    ontology = self._get_ontology()
    if not self.validation_only:
      print("Building knowledge graph...")
      graph = self._build_knowledge_graph(ontology, document)
      print("Knowledge graph built. Storing in Neo4j...")
      self._store_in_neo4j(graph)
      print("Data stored in Neo4j.")
    else: # Get data from Neo4j
      set_graph(self.document_name, self.domain)
    labels = self.neo4j_connection.load_triples_from_neo4j()
    return labels