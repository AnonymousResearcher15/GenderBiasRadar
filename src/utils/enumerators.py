from enum import Enum

class Gender(Enum):
  MASC = 1
  FEM = 2
  NEUT = 3
  UNDEFINED = 4

class Metrics(Enum):
  TP = 1
  FP = 2
  FN = 3
  TN = 4

class Domain(Enum):
  JOB_POSTING = 1
  LEGAL = 2