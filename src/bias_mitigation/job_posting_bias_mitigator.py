from langchain_core.prompts import ChatPromptTemplate
from utils import CustomPromptTemplates
from .bias_mitigator import BiasMitigator
from .custom_rag import CustomRAG

class JobPostingBiasMitigator(BiasMitigator):
  def __init__(self, model_name: str, temperature: float = 0,  rag: CustomRAG = None):
    super().__init__(model_name, temperature, rag)

  def mitigate_bias(self, sentence: str, potentially_biased_word: str = None, entities: str = None) -> str: 
    system_prompt = CustomPromptTemplates().bias_mitigation_jobs_system
    prompt_template = CustomPromptTemplates().bias_mitigation_jobs_prompt
    retrieved_examples = self.rag.retrieve_examples(n_per_rule=1) 
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
    response = chain.invoke({ "content": sentence, "potentially_biased_word": potentially_biased_word, "retrieved_examples": retrieved_examples}).content
    return response