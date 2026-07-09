import nltk
from nltk.tokenize import PunktSentenceTokenizer
import os
from spacy.ml import List
from .chunks_generator import ChunksGeneratorInterface
import pandas as pd

class SentencesGenerator(ChunksGeneratorInterface):
  def __init__(self, document_name: str):
    self.document_name = document_name
    self.file_extension = self._get_file_extension()
  

  def _get_file_extension(self) -> str:
    return self.document_name.split('.')[-1].lower()
  

  def _load_document(self) -> str:
    if self.file_extension == 'txt':
      return self._load_from_txt()
    elif self.file_extension in ['xlsx', 'xls']:
      return self._load_from_excel()


  def _load_from_txt(self) -> str:
    with open(self.document_name, 'r', encoding='utf-8') as file:
      return file.read().replace('\n', ' ')
    

  def _load_from_excel(self) -> List[str]:
    sheet_name = 0
    data = pd.read_excel(self.document_name, sheet_name=sheet_name)
    data["rule_id"] = data["rule_id"].apply(
      lambda x: f"1.{x.month}" if pd.notna(x) else x
    )
    sentences = []
    for data in data.itertuples():
      sentences.append((data.sentence, data.rule_id))
    return sentences


  def get_chunks(self) -> List[str]:
    GREEK_LEGAL_ABBREVIATIONS = [
      'κ.ποιν.δ', 'εφετ', 'κακ', 'παρ', 'αριθ', 'αρ', 'άρθρ', 'άρθ',
      'σελ', 'τμ', 'τόμ', 'χρ', 'ν', 'π.δ', 'β.δ', 'α.ν', 'υ.α',
      'κ.ν', 'εισ', 'εκδ', 'πρβλ', 'βλ', 'σ', 'κεφ', 'υπ',
    ]
    document = self._load_document()
    if self.file_extension == 'txt':
      # nltk.download('punkt_tab')  
      # return nltk.sent_tokenize(document)
      tokenizer = PunktSentenceTokenizer()
      tokenizer._params.abbrev_types.update(GREEK_LEGAL_ABBREVIATIONS)
      return tokenizer.tokenize(document)
    else:
      return self._load_from_excel()