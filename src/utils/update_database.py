from infrastructure.neo4jconnector import Neo4jConnection

def set_graph(graph, domain, neo4j_connection: Neo4jConnection):
  with open(graph, 'r', encoding='utf-8') as file:
    graph = file.read()

  neo4j_connection.store_graph(graph, domain)
  print("Neo4j updated with new graph data.")
