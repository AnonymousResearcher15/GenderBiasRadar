from .bias_detector_service import BiasDetectorService
from bias_mitigation import BiasMitigatorInterface
from text_splitters import ChunksGeneratorInterface
from .embeddings_bias_detection import EmbeddingsGenderBiasDetector
from bias_mitigation import EntitiesExtractor
from text_splitters import NodesGenerator
from .lexicographical_bias_detection import LexicographicalBiasDetector


class LegalBiasDetectorService(BiasDetectorService):
  def __init__(self, 
              document_path: str, 
              bias_mitigator: BiasMitigatorInterface, 
              chunks_generator: ChunksGeneratorInterface, 
              nodes_generator: NodesGenerator, 
              entities_extractor: EntitiesExtractor, 
              embeddings_bias_detector: EmbeddingsGenderBiasDetector, 
              lexicographical_bias_detector: LexicographicalBiasDetector, 
              model_name: str,
              mitigation_model_name: str,
              threshold: float = 0.02,     
              word_threshold: float = 0.03): 
    super().__init__(document_path=document_path, bias_mitigator=bias_mitigator, model_name=model_name)
    self.chunks_generator = chunks_generator
    self.nodes_generator = nodes_generator
    self.entities_extractor = entities_extractor
    self.embeddings_bias_detector = embeddings_bias_detector
    self.lexicographical_bias_detector = lexicographical_bias_detector
    self.mitigation_model_name = mitigation_model_name
    self.threshold = threshold
    self.word_threshold = word_threshold


  def _find_trully_biased_words(self, node_analysis: dict) -> dict:
    """Identify truly biased words by cross-referencing embedding bias scores with lexicographical bias validation."""
    truly_biased_words = []
    for bw in node_analysis['biased_words']:
      if('PROPN' in bw['type']):
        continue
      if (bw['bias_direction'] in bw['bias_lexicographical_direction'] or bw['bias_lexicographical_direction'] is set()) and bw['bias_score'] > self.word_threshold:
        truly_biased_words.append(bw)
    return {
			'sentence': node_analysis['sentence'],
			'overall_bias_score': node_analysis['overall_bias_score'],
			'overall_bias_direction': node_analysis['overall_bias_direction'],
			'is_biased': node_analysis['is_biased'],
			'biased_words': truly_biased_words
		}
  
  def _define_gender(self, genders: list) -> str:
    """Convert bias direction to human readable gender."""
    string_to_return = []
    for gender in genders:
      if gender == 'MASC':
        string_to_return.append('Άνδρες')
      elif gender == 'FEM':
        string_to_return.append('Γυναίκες')
      else:
        string_to_return.append('Άγνωστο')
    return ", ".join(string_to_return)


  def run(self):
    self.nodes_generator.get_chunks()
    entities = self.entities_extractor.extract_entities()
    sentences = self.chunks_generator.get_chunks()
    print("\n" + "=" * 60)
    print("SENTENCE-LEVEL BIAS ANALYSIS")
    print("=" * 60)
    results = ""
    for sentence in sentences:
      embeddings_results = self.embeddings_bias_detector.analyze_sentence(sentence, self.threshold, self.word_threshold)
      lexicographical_analysis = self.lexicographical_bias_detector.perform_validation(embeddings_results)
      node_analysis = self._find_trully_biased_words(lexicographical_analysis)
      sentence_has_bias = self.define_bias(node_analysis)
      if(sentence_has_bias):
        corrected_label = self.mitigate_bias(sentence, entities)
      
      logs = self.generate_logs(node_analysis, sentence_has_bias, corrected_label if sentence_has_bias else None)
      results += logs
      results +="\n"
      print(logs)
    self.store_results_in_txt(results, self.mitigation_model_name)