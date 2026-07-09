from infrastructure import Neo4jConnection
from infrastructure import SqlLiteConnection

class EntitiesExtractor:
  def __init__(self, neo4j_connection: Neo4jConnection, db_connection: SqlLiteConnection):
    self.neo4j = neo4j_connection
    self.db = db_connection
    self.sql_query = "SELECT DISTINCT gender FROM words WHERE form = ?"

  
  def format_entities(self, entities: list[dict]) -> str:
    formatted = []
    for entity in entities:
      raw_gender = entity['gender']
      gender = "Aνδρας" if raw_gender == "Masc" else "Γυναίκα" if raw_gender == "Fem" else "Aνδρας"
      formatted.append(f"-{entity['legal_role']}-> {entity['name']}, {gender}")
    return "\n".join(formatted)
  

  def get_available_labels(self):
    """Get all labels currently in the database."""
    labels = self.neo4j.run_query("CALL db.labels()")
    return [record['label'] for record in labels] 


  def get_triples(self):
    """Query only labels that exist."""
    available_labels = self.get_available_labels()
    
    # Define all possible legal roles
    all_roles = {
        'VicePresidentJudge': 'Aντιπρόεδρος - Δικαστής',
        'SupremeCourtJudge': 'Αρεοπαγίτης - Δικαστής',
        'RapporteurJudge': 'Εισηγητής - Δικαστής',
        'DeputyProsecutor': 'Αντιεισαγγελέας',
        'Prosecutor': 'Εισαγγελέας',
        'Judge': 'Δικαστής',
        'Clerk': 'Γραμματέας',
        'Lawyer': 'Δικηγόρος',
        'Counsel': 'Πληρεξούσιος Δικηγόρος',
        'Defendant': 'Κατηγορούμενος - Αναιρεσειών',
        'CivilClaimant': 'πολιτικώς ενάγων/ενάγουσα'
    }
    
    # Filter to only available labels
    existing_roles = {k: v for k, v in all_roles.items() if k in available_labels}
    
    if not existing_roles:
        return []
    
    # Build query with only existing labels
    where_clause = " OR ".join([f"p:{label}" for label in existing_roles.keys()])
    case_clause = "\n        ".join([
        f"WHEN p:{label} THEN '{role}'" 
        for label, role in existing_roles.items()
    ])
    
    query = f"""
        MATCH (p)
        WHERE {where_clause}
        RETURN 
          p.hasValue AS name,
          CASE 
            {case_clause}
          END AS legal_role
        ORDER BY name
    """
    results = self.neo4j.run_query(query)
    return results
      # return [dict(record) for record in result]


  def extract_entities(self) -> list[dict]:
    triples = self.get_triples()
    entities = []
    for triple in triples:
      if not triple['name'] or not triple['legal_role']:
        continue
      first_name = triple['name'][0].split()[0]
      gender_query_result= self.db.run_query(self.sql_query, (first_name,))
      gender = gender_query_result[0]['gender'] if gender_query_result else 'Unknown'
      entities.append({
        'name': triple['name'][0],
        'legal_role': triple['legal_role'],
        'gender': gender
      })
    return self.format_entities(entities)

