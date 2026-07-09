from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from setuptools import namespaces

class OntologyAnalyzer:
  def __init__(self, path: str):
    self.g = Graph()
    self.ontology = self.g.parse(path)


  def get_classes(self, withUri: bool = False) -> list:
    q_classes = prepareQuery("""
      SELECT ?class
      WHERE {
          ?class a owl:Class .
          FILTER(isIRI(?class))
      }
    """)

    classes_list = []
    for row in self.ontology.query(q_classes):
      if withUri:
        classes_list.append(f"{self.ontology.compute_qname(row[0])[2]}:{self.ontology.compute_qname(row[0])[2]}") 
      else:
        classes_list.append(self.ontology.compute_qname(row[0])[2])
    return classes_list 
  

  def get_object_properties(self, withUri: bool = False) -> list:
    q_object_props = prepareQuery("""
      SELECT ?prop ?domain ?range
      WHERE {
          ?prop a owl:ObjectProperty .
          OPTIONAL { ?prop rdfs:domain ?domain . }
          OPTIONAL { ?prop rdfs:range ?range . }
      }
      ORDER BY ?prop
    """)
    obj_properties_list = []
    for row in self.ontology.query(q_object_props):
      prop_name = self.ontology.compute_qname(row.prop)[2] if not withUri else f"{self.ontology.compute_qname(row.prop)[0]}:{self.ontology.compute_qname(row.prop)[2]}"
      if withUri:
        domain_name = f"{self.ontology.compute_qname(row.domain)[0]}:{self.ontology.compute_qname(row.domain)[2]}" if row.domain else "ANY"
        range_name = f"{self.ontology.compute_qname(row.range)[0]}:{self.ontology.compute_qname(row.range)[2]}" if row.range else "ANY"
      else:
        domain_name = self.ontology.compute_qname(row.domain)[2] if row.domain else "ANY"
        range_name = self.ontology.compute_qname(row.range)[2] if row.range else "ANY"
      
      obj_properties_list.append(f"- {prop_name} (domain: {domain_name}, range: {range_name})")
    return obj_properties_list
  

  def get_data_properties(self, withUri: bool = False) -> list:
    q_data_props = prepareQuery("""
      SELECT ?prop ?domain ?range
      WHERE {
          ?prop a owl:DatatypeProperty .
          OPTIONAL { ?prop rdfs:domain ?domain . }
          OPTIONAL { ?prop rdfs:range ?range . }
      }
      ORDER BY ?prop
    """)

    data_properties_list = []
    for row in self.ontology.query(q_data_props):
      prop_name = self.ontology.compute_qname(row.prop)[2] if not withUri else f"{self.ontology.compute_qname(row.prop)[0]}:{self.ontology.compute_qname(row.prop)[2]}"
      if withUri:
        domain_name = f"{self.ontology.compute_qname(row.domain)[0]}:{self.ontology.compute_qname(row.domain)[2]}" if row.domain else "ANY"
        range_name = f"{self.ontology.compute_qname(row.range)[0]}:{self.ontology.compute_qname(row.range)[2]}" if row.range else "ANY"
      else:
        domain_name = self.ontology.compute_qname(row.domain)[2] if row.domain else "ANY"
        range_name = self.ontology.compute_qname(row.range)[2] if row.range else "ANY"
      
      data_properties_list.append(f"- {prop_name} (domain: {domain_name}, range: {range_name})")
    return data_properties_list
  
  def get_namespaces(self, as_dict: bool = False, only_custom: bool = True):
    """
    Get all namespaces from the ontology.
    
    Args:
      as_dict: If True, returns dict {prefix: namespace}, else returns list of tuples
      only_custom: If True, filters out rdflib's default namespaces
    
    Returns:
      dict or list of (prefix, namespace) tuples
    """
    # Get all namespaces
    all_namespaces = list(self.g.namespace_manager.namespaces())
    
    if only_custom:
      # Filter out rdflib's built-in namespaces
      default_prefixes = {
        'brick', 'csvw', 'dc', 'dcat', 'dcmitype', 'dcterms', 'dcam',
        'doap', 'foaf', 'geo', 'odrl', 'org', 'prof', 'prov', 'qb',
        'schema', 'sh', 'skos', 'sosa', 'ssn', 'time', 'vann', 'void', 'wgs'
      }
      namespaces = [(prefix, ns) for prefix, ns in all_namespaces 
                    if prefix not in default_prefixes]
    else:
      namespaces = all_namespaces
    
    if as_dict:
      return {prefix: str(namespace) for prefix, namespace in namespaces}
    return namespaces
  
  
  def get_ontology_summary(self, withUri : bool = False) -> str:
    """
    Queries the rdflib Graph to extract a concise summary of the ontology's
    classes, object properties, and data properties.
    """

    namespaces = self.get_namespaces()
    summary = "### Ontology Schema ###\n\n"
    for ns in namespaces:
      summary += f"@prefix {ns[0]}: <{ns[1]}> .\n"
    # Format Classes
    summary += "## Classes (Entities you can create):\n"
    for cls in self.get_classes(withUri):
      summary += f"- {cls}\n"
      
    # Format Object Properties
    summary += "\n## Object Properties (Relationships between entities):\n"
    for prop in self.get_object_properties(withUri):
      summary += f"{prop}\n"
      
    # Format Data Properties
    summary += "\n## Data Properties (Attributes of entities):\n"
    for prop in self.get_data_properties(withUri):
      summary += f"{prop}\n"
      
    summary += "######################\n\n"
    
    return summary