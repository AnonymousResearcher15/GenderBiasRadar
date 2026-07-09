from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from utils import CustomPromptTemplates, Domain
import nltk
import re


class Graph(BaseModel):
  triples: str = Field(..., description="The RDF triples in Turtle format representing the knowledge graph.")


class KGBuilder:
  def __init__(self, 
               model_name: str,
               validator_model_name: str = "gemma4:26b", 
               temperature: float = 0,
               domain: Domain = None,
               ontology: str = None,
               document: str = None):
    self.llm = ChatOllama(model=model_name, temperature=temperature, reasoning=False)
    self.validator_llm = ChatOllama(model=validator_model_name, temperature=0.0, reasoning=False)
    self.domain = domain
    self.ontology = ontology
    self.document = document

  def _split_into_sentences(self, document: str) -> dict[int, str]:
    nltk.download('punkt_tab')  # One-time download of the data model
    sentences = nltk.sent_tokenize(document)
    for sentence in sentences:
      if sentence.strip() == '':
        sentences.remove(sentence)
    sentences = {index: sentence.strip() for index, sentence in enumerate(sentences)}
    return sentences

  def _extract_turtle_block(self, text: str) -> str:
    if not text:
      return ""
    pattern = r"```(?:turtle|tutle)\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
      return match.group(1).strip()
    return text.strip()

  def build_kg(self) -> str:
    sentences = self._split_into_sentences(self.document)
    system = CustomPromptTemplates().kg_bulder_system_prompt
    prompt_template = CustomPromptTemplates().kg_bulder_content_prompt_legal
    examples = CustomPromptTemplates().job_posting_example if self.domain == Domain.JOB_POSTING else CustomPromptTemplates().legal_example
    prompt = ChatPromptTemplate.from_messages(
      [
        {
          'role': 'system',
          'content': system,
        },
        {
          'role': 'user',
          'content': prompt_template,
        }
      ]
    )

    chain = prompt | self.llm
    triples = ""
    graph = ""
    for index, content in sentences.items():
      print(f"\nProcessing Sentence {index}: {content}")
      triples = chain.invoke({"ontology": self.ontology, "examples": examples, "content": f"{index}: {content}", "graph": graph}).content
      extracted = self._extract_turtle_block(triples)
      print(f"\nNew triples:\n {extracted}")
      graph += extracted + "\n"
      print(f"\nUpdated Graph:\n{graph}")
    return graph
  

  def validate_graph(self, graph: str, ontology: str = None) -> str:
    system_evaluator = CustomPromptTemplates().system_evaluator
    evaluator_prompt_template = CustomPromptTemplates().evaluator_prompt_template
    
    prompt_evaluator = ChatPromptTemplate.from_messages(
        [
            ('system', system_evaluator),
            ('user', evaluator_prompt_template)
        ]
    )

    chain_evaluator = prompt_evaluator | self.validator_llm.with_structured_output(Graph, method="json_schema")

    validated_graph = []

    # Invoke the chain
    graph_splits = graph.split(" .")
    for split in graph_splits:
      print(f"\nEvaluating split:\n{split}\n")
      result = chain_evaluator.invoke({"ontology": ontology or "", "graph": split})
      validated_graph.append(result.triples)

    print("\n\n--- FINAL CORRECTED GRAPH ---\n")
    print("\n".join(validated_graph))
    return "\n".join(validated_graph)