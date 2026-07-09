import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional
import spacy
from langdetect import detect, LangDetectException
from utils import Gender

class EmbeddingsGenderBiasDetector:
  def __init__(self, 
               model_name: str = 'lighteternal/stsb-xlm-r-greek-transfer',
               nlp_model: Optional[str] = "el_core_news_lg",
               method: str = 'centroid',
               male_terms: list[str] = None,
               female_terms: list[str] = None,
               male_stereotyped_professions: Optional[list[str]] = None,
               female_stereotyped_professions: Optional[list[str]] = None):
    self.model = SentenceTransformer(model_name)
    self.nlp_model = spacy.load(nlp_model)
    self.male_terms = male_terms
    self.female_terms = female_terms
    self.male_stereotyped_professions = male_stereotyped_professions
    self.female_stereotyped_professions = female_stereotyped_professions
    self.method = method
    
    self._compute_set_embeddings()
    

  def _compute_set_embeddings(self):
    """Compute and store embeddings for all word sets."""
    self.male_embeddings = self.model.encode(self.male_terms)
    self.female_embeddings = self.model.encode(self.female_terms)
        
    # Compute centroid (average) embeddings for each set
    self.male_terms_centroid = np.mean(self.male_embeddings, axis=0)
    self.female_terms_centroid = np.mean(self.female_embeddings, axis=0)
    

  def compute_gender_association(self, word: str, threshold: float = 0.02) -> dict:
    """
    Compute how strongly a word is associated with male vs female concepts.
    
    Returns:
        Dictionary with similarity scores and bias direction
    """
    word_embedding = self.model.encode([word])[0]

    if self.method == 'centroid':
      sim_male = cosine_similarity([word_embedding], [self.male_terms_centroid])[0][0]
      sim_female = cosine_similarity([word_embedding], [self.female_terms_centroid])[0][0]
    else:
      sim_male = self._calculate_mean_cosine_similarity(word_embedding, self.male_embeddings)
      sim_female = self._calculate_mean_cosine_similarity(word_embedding, self.female_embeddings)
    
    # Bias score: positive = male bias, negative = female bias
    bias_score = sim_male - sim_female
    
    return {
      'word': word,
      'bias_score': float(bias_score),
      'bias_direction': Gender.MASC.name if bias_score > threshold else (Gender.FEM.name if bias_score < -threshold else Gender.NEUT.name)
    }
  

  def _get_selected_words(self, words: list[str]) -> list[str]:
    selected = []
    for word in words:
      if not self._is_greek_word(word):
        continue
      if '/' in word:
        selected.append(word)
        continue
      doc = self.nlp_model(word.strip())
      if len(doc) == 0:
        continue
      token = doc[0]
      if token.pos_ in ['NOUN', 'ADJ', 'PROPN', 'ADV']:
        selected.append(token.text)
    return selected
  
  def _is_greek_word(self, word: str) -> bool:
    try:
      return detect(word) == 'el'
    except LangDetectException:
      return False
    
  
  def _remove_non_greek_words(self, sentence: str) -> str:
    """Remove non-Greek words from the sentence."""
    words = sentence.split()
    greek_words = [word for word in words if self._is_greek_word(word)]
    return ' '.join(greek_words)
    

  def _calculate_mean_cosine_similarity(self, word_embedding, reference_embeddings):
    total_similarity = 0.0
    for emb in reference_embeddings:
      total_similarity += cosine_similarity([word_embedding], [emb])[0][0]
    return total_similarity / len(reference_embeddings)
    

  def analyze_sentence(self, sentence: str, threshold: float = 0.02, word_threshold: float = 0.03) -> dict:
    """
    Analyze a job offer sentence for gender bias.
    
    Args:
        sentence: The job offer text in Greek
        threshold: Minimum bias score to flag (default 0.02)
        word_threshold: Minimum bias score for individual words (default 0.03)
        
    Returns:
        Analysis results with detected biases
    """
    # Remove non-Greek words from the sentence
    sentence_to_evaluate = self._remove_non_greek_words(sentence)
    
    # Get sentence embedding
    
    sentence_embedding = self.model.encode([sentence_to_evaluate])[0]
    
    # Compute associations
    if self.method == 'centroid':
      sim_male = cosine_similarity([sentence_embedding], [self.male_terms_centroid])[0][0]
      sim_female = cosine_similarity([sentence_embedding], [self.female_terms_centroid])[0][0]
    else:
      sim_male = self._calculate_mean_cosine_similarity(sentence_embedding, self.male_embeddings)
      sim_female = self._calculate_mean_cosine_similarity(sentence_embedding, self.female_embeddings)
    
    bias_score = sim_male - sim_female
    
    # Also analyze individual words in the sentence
    words = sentence.split()
    clean_words = self._get_clean_word(words)
    selected_words = self._get_selected_words(clean_words)
    biased_words = []
    for word in selected_words:
      if len(word) > 2:
        if '/' in word:
         biased_words.append({
          'word': word,
          'bias_score': float(0.0),
          'bias_direction': Gender.NEUT.name
         })
         continue
        word_analysis = self.compute_gender_association(word, threshold=threshold)
        if abs(word_analysis['bias_score']) > threshold:
          biased_words.append(word_analysis)
    
    biased_words_sorted = sorted(biased_words, key=lambda x: abs(x['bias_score']), reverse=True)
    return {
      'sentence': sentence,
      'overall_bias_score': float(bias_score),
      'overall_bias_direction': Gender.MASC.name if bias_score > threshold else (Gender.FEM.name if bias_score < -threshold else Gender.NEUT.name),
      'biased_words': biased_words_sorted,
      'is_biased': abs(bias_score) > threshold or self._bias_in_words(biased_words_sorted, word_threshold)
    }
  
  def _get_clean_word(self, words: list[str]) -> list[str]:
    return [word.strip('«».,;:!?()[]{}') for word in words]
  
  def _bias_in_words(self, words: list[dict], threshold: float) -> bool:
    for word in words:
      if abs(word['bias_score']) > threshold:
        return True
    return False
    