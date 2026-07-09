from langchain_ollama import ChatOllama
from .bias_mitigator import BiasMitigator
from .custom_rag import CustomRAG
from utils import CustomPromptTemplates
from langchain_core.prompts import ChatPromptTemplate

class LegalBiasMitigator(BiasMitigator):
  def __init__(self, 
    model_name: str, 
    temperature: float = 0, 
    rag: CustomRAG = None):
    super().__init__(model_name, temperature, rag)

  def mitigate_bias(self, sentence: str, entities: str = None) -> str: 
    system_prompt = CustomPromptTemplates().bias_mitigation_legal_system
    prompt_template = CustomPromptTemplates().bias_mitigation_legal_prompt
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
    response = chain.invoke({ "content": sentence, "entities": entities }).content
    return response