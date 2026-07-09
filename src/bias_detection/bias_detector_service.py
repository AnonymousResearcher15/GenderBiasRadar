from bias_mitigation import BiasMitigator
import os


class BiasDetectorServiceInterface:
  def mitigate_bias(self):
    pass

  def define_bias(self):
    pass

  def generate_logs(self):
    pass

  def run(self):
    pass


class BiasDetectorService(BiasDetectorServiceInterface):
  def __init__(self, document_path: str, bias_mitigator: BiasMitigator, model_name: str):
    self.document_path = document_path
    self.bias_mitigator = bias_mitigator
    self.model_name = model_name

  def _get_file_name(self) -> str:
    return os.path.splitext(os.path.basename(self.document_path))[0]


  def _extract_potentially_biased_word(self, node_analysis:dict) -> str:
    """Extract the most potentially biased word from the node analysis."""
    if not node_analysis['biased_words']:
      return None
    terms = set(bw['word'] for bw in node_analysis['biased_words'])
    return ", ".join(terms)
  

  def store_results_in_txt(self, logs: str, model_name: str):
    file_name = self._get_file_name()
    results_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    output_path = os.path.join(results_dir, f"{file_name}_{model_name.replace(':', '_')}_analysis.txt")
    print(f"\nStoring results in 'results/{file_name}_{model_name}_analysis.txt'...")
    with open(output_path, 'a', encoding='utf-8') as f:
      f.write(logs)

  def mitigate_bias(self, sentence: str, entities: str = None, potentially_biased_word: str = None) -> str:
    return self.bias_mitigator.mitigate_bias(sentence, entities)
    

  def define_bias(self, node_analysis) -> bool:
    number_of_biased_words = len(node_analysis['biased_words'])

    if node_analysis['overall_bias_score'] > self.threshold and number_of_biased_words > 0 and node_analysis['overall_bias_direction'] in [bw['bias_direction'] for bw in node_analysis['biased_words']]:
      return True
    
    if number_of_biased_words > 0 and any(bw['bias_score'] > self.threshold for bw in node_analysis['biased_words']):
      return True
    
    return False


  def generate_logs(self, node_analysis: dict, label_has_bias: bool, unbiased_label: str = None) -> str:
    logs = ""
    logs += f"\n📄 '{node_analysis['sentence']}'"
    logs += "\nWord Embeddings Bias Analysis:"
    logs += f"\n   → Overall bias: {node_analysis['overall_bias_score']:+.4f} ({node_analysis['overall_bias_direction']})"
    logs += f"\n   → Is biased: {'⚠️ YES' if node_analysis['is_biased'] else '✅ NO'}"
    biased_words_count = len(node_analysis['biased_words'])
    logs += f"\n   → Biased words detected: {biased_words_count}"

    if biased_words_count > 0:
      logs += f"\nLexicographical Analysis:"
      logs += f"\n   → Biased words details:"
      for bw in node_analysis['biased_words']:
        logs += f"\n      • '{bw['word']}': {bw['bias_score']:+.4f} ({bw['bias_direction']})" 
        logs += f"- Lexicographical bias: {'⚠️ YES' if bw['bias_lexicographical_direction'] == bw['bias_direction'] else '✅ NO'} (Direction: {bw['bias_lexicographical_direction']})"
        logs += f"- Type: {', '.join(bw['type']) if bw['type'] else 'N/A'}"
    
    logs += "\nFinal Assessment:"
    if label_has_bias:
      logs += "\n   → Overall bias: ⚠️ YES"
    else:
      logs += "\n   → Overall bias: ✅ NO"
    if unbiased_label:
      logs += f"\n   → Corrected label: {unbiased_label}"
    return logs


  def run(self):
    pass


  def _find_trully_biased_words(self, node_analysis: dict) -> dict:
    pass