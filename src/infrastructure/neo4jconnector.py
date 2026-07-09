from neo4j import GraphDatabase
from utils import Domain

# Define the Neo4j database connection class
class Neo4jConnection:

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def initialize(self):
        self.run_query("MATCH (n) DETACH DELETE n")
        self.run_query("CALL n10s.nsprefixes.removeAll()")
        self.run_query("CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS FOR (r:Resource) REQUIRE r.uri IS UNIQUE")
        self.run_query("""CALL n10s.graphconfig.init({
            handleVocabUris: 'MAP',
            handleMultival: 'ARRAY',
            keepLangTag: true,
            handleRDFTypes: 'LABELS'})
        """)
        

    def set_namespace_prefix(self, prefix, namespace):
        """Set namespace prefix for easier querying"""
        query = """
        CALL n10s.nsprefixes.add($prefix, $namespace)
        """
        self.run_query(query, {"prefix": prefix, "namespace": namespace})
        print(f"Added prefix '{prefix}' for namespace '{namespace}'")

    def close(self):
        self._driver.close()

    def run_query(self, query, params=None):
        with self._driver.session() as session:
            result = session.run(query, params)
            return result.data()  # Fetch all results

    def import_rdf_inline(self, rdf_data, format="Turtle"):
        """Import RDF data from a string"""
        query = """CALL n10s.rdf.import.inline($rdf, $format)"""
        results = self.run_query(query, {"rdf": rdf_data, "format": format})
        return results

    def store_graph(self, graph_data, domain: Domain, format="Turtle"):
        """Store RDF graph data into Neo4j"""
        self.initialize()
        if domain == Domain.JOB_POSTING:
            self.set_namespace_prefix("job", "http://example.org/job-ontology#")
        elif domain == Domain.LEGAL:
            self.set_namespace_prefix("ld", "http://example.org/legal-domain#")
        self.set_namespace_prefix("xsd", "http://www.w3.org/2001/XMLSchema#")
        if "@prefix" not in graph_data:
            if domain == Domain.JOB_POSTING:
                prefixes = (
                    "@prefix job: <http://example.org/job-ontology#> .\n"
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n"
                )
            elif domain == Domain.LEGAL:
                prefixes = (
                    "@prefix ld: <http://example.org/legal-domain#> .\n"
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n"
                )
            graph_data = prefixes + graph_data
        results = self.import_rdf_inline(graph_data)
        if results:
            status = results[0].get("terminationStatus")
            triples_loaded = results[0].get("triplesLoaded")
            if status and status != "OK":
                raise RuntimeError(f"Neo4j RDF import failed: {results[0]}")
            if triples_loaded == 0:
                raise RuntimeError(f"Neo4j RDF import loaded 0 triples: {results[0]}")
        self.close()
        return True
    
    def load_triples_from_neo4j(self) -> list:
        query = """ 
        MATCH (n) WHERE n.hasName is not null  RETURN n.hasName  AS label, n.uri AS uri, n.sentenceId AS sentenceId
        UNION
        MATCH (n) WHERE n.hasTitle is not null  RETURN n.hasTitle  AS label, n.uri AS uri, n.sentenceId AS sentenceId
        UNION
        MATCH (n) WHERE n.hasValue is not null  RETURN n.hasValue  AS label, n.uri AS uri, n.sentenceId AS sentenceId
        """
        results = self.run_query(query)
        labels = []
        for result in results:
            labels.append(result['label'][0])
        return labels