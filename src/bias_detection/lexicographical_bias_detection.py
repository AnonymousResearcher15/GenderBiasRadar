from infrastructure import SqlLiteConnection
from utils import Gender

class LexicographicalBiasDetector:
	"""Class to validate the semantic bias of sentences based on a database of words."""
	def __init__(self, db_connector: SqlLiteConnection, bias_threshold: float = 0.02) -> None:
		self.connector = db_connector
		self.bias_threshold = bias_threshold


	def perform_validation(self, node: dict) -> dict:
		if len(node['biased_words']) == 0:
			return node
		
		updated_biased_words = []
		for biased_word in node['biased_words']:
			word_lexicographical_info = self.connector.get_gender_list(biased_word['word'])
	    
			if not word_lexicographical_info:
				updated_biased_word = {
					'word': biased_word['word'], 
					'bias_score': biased_word['bias_score'], 
					'bias_direction': biased_word['bias_direction'],
					'has_lexicographical_bias': None,
					'bias_lexicographical_direction': None,
					'type': None
				}
			else:
				genders = list(row['gender'] for row in word_lexicographical_info)
				
				words = node['sentence'].split()
				words = [word.strip('«».,;:!?()[]{}"') for word in words]
				
				index = words.index(biased_word['word'])
				sentence_to_evaluate = biased_word['word'] if index == 0 else f"{words[index-1]} {biased_word['word']}"
				
				bias_evaluation = self._gender_bias_exists(sentence_to_evaluate, genders)
				updated_biased_word = {
					'word': biased_word['word'], 
					'bias_score': biased_word['bias_score'], 
					'bias_direction': biased_word['bias_direction'],
					'has_lexicographical_bias': bias_evaluation['has_bias'],
					'bias_lexicographical_direction': bias_evaluation['bias_direction'],
					'type': set(row['pos'] for row in word_lexicographical_info)
				}
				updated_biased_words.append(updated_biased_word)

		return {
			'sentence': node['sentence'],
			'overall_bias_score': node['overall_bias_score'],
			'overall_bias_direction': node['overall_bias_direction'],
			'is_biased': node['is_biased'],
			'biased_words': updated_biased_words
		}		


	def _gender_bias_exists(self, sentence: str, genders: list[str]) -> dict:
		"""Determine if a sentence contains gender bias based on the results from the database."""
		words = sentence.split()
		determiner = words[0].lower() if len(words) == 2 else None
		main_word = words[1].lower() if len(words) == 2 else words[0].lower()
		# If no determiner or an irrelevant one is found e.g., ως, είναι, etc., use the most popular gender
		if determiner is None or determiner not in ['ο', 'η', 'το', 'τον', 'του', 'την', 'της', 'ο/η', 'η/ο', 'τον/την', 'την/τον']:
			# most_popular = max(genders, key=genders.count)
			# if most_popular in ['Masc', 'Fem']:
				# gender = Gender.MASC.name if most_popular == 'Masc' else Gender.FEM.name
				# gender = Gender.NEUT.name if most_popular == 'Neut' else gender
				# return {'has_bias': True, 'bias_direction': gender}
			# else:
			return {'has_bias': False, 'bias_direction': set(gender.upper() for gender in genders if gender is not None) if genders else set()}
		if "/" in determiner or "/" in main_word:
			return {'has_bias': False, 'bias_direction': Gender.NEUT.name}
		if determiner in ['ο', 'του', 'τον'] and "Masc" in genders:
			return {'has_bias': True, 'bias_direction': Gender.MASC.name}
		if determiner in ['η', 'της', 'την'] and "Fem" in genders or "Masc" in genders:
			return {'has_bias': True, 'bias_direction': Gender.FEM.name}	
		if determiner in ['το'] and "Neut" in genders:
			return {'has_bias': False, 'bias_direction': Gender.NEUT.name}

		return {'has_bias': False, 'bias_direction': Gender.NEUT.name}

