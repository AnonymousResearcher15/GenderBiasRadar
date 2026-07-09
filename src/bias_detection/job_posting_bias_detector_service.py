from .bias_detector_service import BiasDetectorService
from .embeddings_bias_detection import EmbeddingsGenderBiasDetector
from text_splitters import NodesGenerator
from .lexicographical_bias_detection import LexicographicalBiasDetector
from infrastructure import SqlLiteConnection
from bias_mitigation import BiasMitigatorInterface

class JobPostingBiasDetectorService(BiasDetectorService):
  def __init__(self,
               document_path: str, 
               bias_mitigator: BiasMitigatorInterface, 
               db_connector: SqlLiteConnection,
               nodes_generator: NodesGenerator,
               embeddings_bias_detector: EmbeddingsGenderBiasDetector,
               lexicographical_bias_detector: LexicographicalBiasDetector,
               model_name: str,
               mitigation_model_name: str = None,
               threshold: float = 0.02,     
               word_threshold: float = 0.03):
    super().__init__(document_path=document_path, bias_mitigator=bias_mitigator, model_name=model_name)
    self.db_connector = db_connector
    self.nodes_generator = nodes_generator
    self.embeddings_bias_detector = embeddings_bias_detector
    self.lexicographical_bias_detector = lexicographical_bias_detector
    self.mitigation_model_name = mitigation_model_name
    self.threshold = threshold
    self.word_threshold = word_threshold


  def _find_trully_biased_words(self, node_analysis: dict) -> dict:
    """Identify truly biased words by cross-referencing embedding bias scores with lexicographical bias validation."""
    truly_biased_words = []
    for bw in node_analysis['biased_words']:
      if bw['bias_direction'] in bw['bias_lexicographical_direction'] or bw['bias_lexicographical_direction'] is set():
        truly_biased_words.append(bw)
    return {
			'sentence': node_analysis['sentence'],
			'overall_bias_score': node_analysis['overall_bias_score'],
			'overall_bias_direction': node_analysis['overall_bias_direction'],
			'is_biased': node_analysis['is_biased'],
			'biased_words': truly_biased_words
		}		 
  

  def run(self):
    nodes = self.nodes_generator.get_chunks()
    print("\n" + "=" * 60)
    print("NODE-LEVEL BIAS ANALYSIS")
    print("=" * 60)
    results = ""
    for label in nodes:
      embeddings_results = self.embeddings_bias_detector.analyze_sentence(label, self.threshold, self.word_threshold)
      lexicographical_analysis = self.lexicographical_bias_detector.perform_validation(embeddings_results)
      node_analysis = self._find_trully_biased_words(lexicographical_analysis)
      node_has_bias = self.define_bias(node_analysis)
      
      if(node_has_bias):
        potentially_biased_word = self._extract_potentially_biased_word(node_analysis)
        corrected_label = self.mitigate_bias(label, potentially_biased_word)
  
      logs = self.generate_logs(node_analysis, node_has_bias, corrected_label if node_has_bias else None)
      results += logs
      results +="\n"
      print(logs)
    self.store_results_in_txt(results, self.mitigation_model_name)
