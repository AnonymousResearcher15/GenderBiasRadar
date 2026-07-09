from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from utils import CustomPromptTemplates
from .custom_rag import CustomRAG

load_dotenv()

class BiasMitigatorInterface:
  def mitigate_bias(self, sentence: str, entities: str = None) -> str:
    pass

class BiasMitigator(BiasMitigatorInterface):
  def __init__(self, model_name: str, temperature: float = 0,  rag: CustomRAG = None):
    self.llm = ChatOllama(model=model_name, temperature=temperature)
    self.rag = rag

  def mitigate_bias(self, sentence: str, entities: str = None) -> str: 
    system_prompt = CustomPromptTemplates().bias_mitigation_legal_system
    prompt_template = CustomPromptTemplates().bias_mitigation_legal_prompt

    # retrieved_examples = self.rag.retrieve_examples(n_per_rule=1) 
    prompt = ChatPromptTemplate.from_messages(
      [
        {
          'role': 'system',
          'content': system_prompt,
        },
        {
          'role': 'user',
          'content': prompt_template,
        }
      ]
    )
    chain = prompt | self.llm
    response = chain.invoke({ "content": sentence, "entities": entities}).content
    return response