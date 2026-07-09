# GenderBiasFramework

An SLM-based framework that combines ontologies, Knowledge Graphs, Embeddings and deterministic methods to effectivelly detect and mitigate gender bias in Greek texts.

## Overview

`GenderBiasFramework` aims to support fairness-aware legal NLP workflows by providing tools to:
- process and clean legal text data,
- identify potentially biased language patterns,
- evaluate model behavior across fairness-related metrics,
- and produce interpretable outputs for analysis.

# System Architecture


# Experimental Results
## Legal Documents
### Detection Module Evaluation 
Gender Bias Detection **without** lexicographical analysis using **Gemma4 (26b)** for text-2-KG transformation 

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 2  | 0  | 0,50      | 1,00   | 0,67     |
| LEGALDOC2 | 1            | 1  | 2  | 0  | 0,33      | 1,00   | 0,50     |
| LEGALDOC3 | 21           | 14 | 11 | 7  | 0,56      | 0,67   | 0,61     |
| LEGALDOC4 | 13           | 13 | 5  | 0  | 0,72      | 1,00   | 0,84     |
| LEGALDOC5 | 4            | 4  | 10 | 0  | 0,29      | 1,00   | 0,44     |
| **Total** |              |    |    |    | **0,48**  | **0,93** | **0,61** |

Gender Bias Detection **with** lexicographical analysis using **Gemma4 (26b)** for text-2-KG transformation

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 1  | 0  | 0,67      | 1,00   | 0,80     |
| LEGALDOC2 | 1            | 1  | 2  | 0  | 0,33      | 1,00   | 0,50     |
| LEGALDOC3 | 21           | 11 | 1  | 10 | 0,92      | 0,52   | 0,67     |
| LEGALDOC4 | 13           | 2  | 3  | 11 | 0,40      | 0,15   | 0,22     |
| LEGALDOC5 | 4            | 4  | 1  | 0  | 0,80      | 1,00   | 0,89     |
| **Total** |              |    |    |    | **0,62**  | **0,74** | **0,62** |


---

Gender Bias Detection **without** lexicographical analysis using **Ministral3 (14b)** for text-2-KG transformation 

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 2  | 0  | 0,50      | 1,00   | 0,67     |
| LEGALDOC2 | 1            | 1  | 2  | 0  | 0,33      | 1,00   | 0,50     |
| LEGALDOC3 | 21           | 14 | 1  | 7  | 0,93      | 0,67   | 0,78     |
| LEGALDOC4 | 13           | 13 | 5  | 0  | 0,72      | 1,00   | 0,84     |
| LEGALDOC5 | 4            | 4  | 10 | 0  | 0,29      | 1,00   | 0,44     |
| **Total** |              |    |    |    | **0,55**  | **0,93** | **0,65** |

Gender Bias Detection **with** lexicographical analysis using **Ministral3 (14b)** for text-2-KG transformation

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 1  | 0  | 0,67      | 1,00   | 0,80     |
| LEGALDOC2 | 1            | 1  | 2  | 0  | 0,33      | 1,00   | 0,50     |
| LEGALDOC3 | 21           | 11 | 1  | 10 | 0,92      | 0,52   | 0,67     |
| LEGALDOC4 | 13           | 2  | 3  | 11 | 0,40      | 0,15   | 0,22     |
| LEGALDOC5 | 4            | 4  | 1  | 0  | 0,80      | 1,00   | 0,89     |
| **Total** |              |    |    |    | **0,62**  | **0,74** | **0,62** |

---

### Mitigation Module Evaluation  
Gender Bias Mitigration analysis of **detected bias** using **OpenEuroLLM-Greek (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| LEGALDOC2 | 1            | 1  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC3 | 11           | 0  | 1  | 11 | 0,00      | 0,00   | 0,00     |
| LEGALDOC4 | 2            | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| LEGALDOC5 | 4            | 1  | 1  | 3  | 0,50      | 0,25   | 0,33     |
| **Total** |              |    |    |    | **0,70**  | **0,45** | **0,53** |


Gender Bias Mitigration analysis of **overall bias** using **OpenEuroLLM-Greek (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| LEGALDOC2 | 1            | 1  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC3 | 21           | 0  | 1  | 21 | 0,00      | 0,00   | 0,00     |
| LEGALDOC4 | 13           | 1  | 0  | 12 | 1,00      | 0,08   | 0,14     |
| LEGALDOC5 | 4            | 1  | 1  | 3  | 0,50      | 0,25   | 0,33     |
| **Total** |              |    |    |    | **0,70**  | **0,37** | **0,43** |

---

Gender Bias Mitigration analysis of **detected bias** using **Llama-Krikri (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC2 | 1            | 1  | 1  | 0  | 0,50      | 1,00   | 0,67     |
| LEGALDOC3 | 11           | 0  | 1  | 11 | 0,00      | 0,00   | 0,00     |
| LEGALDOC4 | 2            | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| LEGALDOC5 | 4            | 1  | 1  | 3  | 0,50      | 0,25   | 0,33     |
| **Total** |              |    |    |    | **0,60**  | **0,55** | **0,53** |

Gender Bias Mitigration analysis of **overall bias** using **Llama-Krikri (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC2 | 1            | 1  | 1  | 0  | 0,50      | 1,00   | 0,67     |
| LEGALDOC3 | 21           | 0  | 1  | 21 | 0,00      | 0,00   | 0,00     |
| LEGALDOC4 | 13           | 1  | 0  | 12 | 1,00      | 0,08   | 0,14     |
| LEGALDOC5 | 4            | 1  | 1  | 3  | 0,50      | 0,25   | 0,33     |
| **Total** |              |    |    |    | **0,60**  | **0,47** | **0,43** |

---

Gender Bias Mitigration analysis of **detected bias** using **Ministral3 (14b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC2 | 1            | 1  | 1  | 0  | 0,50      | 1,00   | 0,67     |
| LEGALDOC3 | 11           | 9  | 1  | 2  | 0,90      | 0,82   | 0,86     |
| LEGALDOC4 | 2            | 2  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC5 | 4            | 2  | 1  | 2  | 0,67      | 0,50   | 0,57     |
| **Total** |              |    |    |    | **0,81**  | **0,86** | **0,82** |

Gender Bias Mitigration analysis of **overall bias** using **Ministral3 (14b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| LEGALDOC1 | 2            | 2  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| LEGALDOC2 | 1            | 1  | 1  | 0  | 0,50      | 1,00   | 0,67     |
| LEGALDOC3 | 11           | 9  | 1  | 12 | 0,90      | 0,43   | 0,58     |
| LEGALDOC4 | 2            | 2  | 0  | 11 | 1,00      | 0,15   | 0,27     |
| LEGALDOC5 | 4            | 2  | 1  | 2  | 0,67      | 0,50   | 0,57     |
| **Total** |              |    |    |    | **0,81**  | **0,62** | **0,62** |


## Job Advertisements
### Detection Module Evaluation 
Gender Bias Detection **without** lexicographical analysis using **Gemma4 (26b)** for text-2-KG transformation 

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7            | 5  | 8  | 2  | 0,38      | 0,71   | 0,50     |
| JOBADS2 | 2            | 1  | 4  | 1  | 0,20      | 0,50   | 0,29     |
| JOBADS3 | 3            | 2  | 6  | 1  | 0,25      | 0,67   | 0,36     |
| JOBADS4 | 2            | 1  | 7  | 1  | 0,13      | 0,50   | 0,20     |
| JOBADS5 | 3            | 2  | 5  | 1  | 0,29      | 0,67   | 0,40     |
| **Total** |            |    |    |    | **0,25**  | **0,61** | **0,35** |

Gender Bias Detection **with** lexicographical analysis using **Gemma4 (26b)** for text-2-KG transformation

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7            | 4  | 4  | 3  | 0,50      | 0,57   | 0,53     |
| JOBADS2 | 2            | 1  | 1  | 0  | 0,50      | 1,00   | 0,67     |
| JOBADS3 | 3            | 2  | 2  | 1  | 0,50      | 0,67   | 0,57     |
| JOBADS4 | 2            | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| JOBADS5 | 3            | 2  | 0  | 1  | 1,00      | 0,67   | 0,80     |
| **Total** |            |    |    |    | **0,70**  | **0,68** | **0,65** |


---

Gender Bias Detection **without** lexicographical analysis using **Ministral3 (14b)** for text-2-KG transformation 

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7            | 7  | 9  | 0  | 0,44      | 1,00   | 0,61     |
| JOBADS2 | 2            | 1  | 3  | 1  | 0,25      | 0,50   | 0,33     |
| JOBADS3 | 3            | 2  | 8  | 1  | 0,20      | 0,67   | 0,31     |
| JOBADS4 | 2            | 0  | 7  | 2  | 0,00      | 0,00   | 0,00     |
| JOBADS5 | 3            | 3  | 6  | 0  | 0,33      | 1,00   | 0,50     |
| **Total** |            |    |    |    | **0,24**  | **0,63** | **0,35** |

Gender Bias Detection **with** lexicographical analysis using **Ministral3 (14b)** for text-2-KG transformation

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7            | 5  | 5  | 2  | 0,50      | 0,71   | 0,59     |
| JOBADS2 | 2            | 1  | 1  | 1  | 0,50      | 0,50   | 0,50     |
| JOBADS3 | 3            | 2  | 2  | 1  | 0,50      | 0,67   | 0,57     |
| JOBADS4 | 2            | 0  | 0  | 2  | 0,00      | 0,00   | 0,00     |
| JOBADS5 | 3            | 2  | 1  | 1  | 0,67      | 0,67   | 0,67     |
| **Total** |            |    |    |    | **0,24**  | **0,51** | **0,47** |

---

### Mitigation Module Evaluation  
Gender Bias Mitigration analysis of **detected bias** using **OpenEuroLLM-Greek (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 4              | 4  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| JOBADS2 | 1              | 1  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| JOBADS3 | 2              | 2  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| JOBADS4 | 1              | 0  | 1  | 1  | 0,00      | 0,00   | 0,00     |
| JOBADS5 | 2              | 0  | 1  | 2  | 0,00      | 0,00   | 0,00     |
| **Total** |              |    |    |    | **0,60**  | **0,60** | **0,60** |


Gender Bias Mitigration analysis of **overall bias** using **OpenEuroLLM-Greek (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7              | 4  | 0  | 3  | 1,00      | 0,57   | 0,73     |
| JOBADS2 | 2              | 1  | 0  | 1  | 1,00      | 0,50   | 0.67     |
| JOBADS3 | 3              | 2  | 0  | 1  | 1,00      | 0,67   | 0,80     |
| JOBADS4 | 2              | 0  | 1  | 2  | 0,00      | 0,00   | 0,00     |
| JOBADS5 | 3              | 0  | 1  | 3  | 0,00      | 0,00   | 0,00     |
| **Total** |              |    |    |    | **0,60**  | **0,35** | **0,44** |

---

Gender Bias Mitigration analysis of **detected bias** using **Llama-krikri (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 4              | 3  | 1  | 1  | 0,75      | 0,75   | 0,75     |
| JOBADS2 | 1              | 1  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| JOBADS3 | 2              | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| JOBADS4 | 1              | 0  | 1  | 1  | 0,00      | 0,00   | 0,00     |
| JOBADS5 | 2              | 0  | 1  | 2  | 0,00      | 0,00   | 0,00     |
| **Total** |              |    |    |    | **0,55**  | **0,45** | **0,48** |


Gender Bias Mitigration analysis of **overall bias** using **Llama-krikri (8b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7              | 3  | 1  | 4  | 0,75      | 0,43   | 0,55     |
| JOBADS2 | 2              | 1  | 0  | 1  | 1,00      | 0,50   | 0.67     |
| JOBADS3 | 3              | 1  | 0  | 2  | 1,00      | 0,33   | 0,50     |
| JOBADS4 | 2              | 0  | 1  | 2  | 0,00      | 0,00   | 0,00     |
| JOBADS5 | 3              | 0  | 1  | 3  | 0,00      | 0,00   | 0,00     |
| **Total** |              |    |    |    | **0,55**  | **0,25** | **0,34** |

---

Gender Bias Mitigration analysis of **detected bias** using **Ministral3 (14b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 4              | 3  | 0  | 1  | 1,00      | 0,75   | 0,86     |
| JOBADS2 | 1              | 1  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| JOBADS3 | 2              | 1  | 0  | 1  | 1,00      | 0,50   | 0,67     |
| JOBADS4 | 1              | 0  | 0  | 0  | 1,00      | 1,00   | 1,00     |
| JOBADS5 | 2              | 0  | 1  | 2  | 0,00      | 0,00   | 0,00     |
| **Total** |              |    |    |    | **0,80**  | **0,65** | **0,70** |


Gender Bias Mitigration analysis of **overall bias** using **Ministral3 (14b)** model

| Document  | Ground Truth | TP | FP | FN | Precision | Recall | F1-score |
|-----------|--------------|----|----|----|-----------|--------|----------|
| JOBADS1 | 7              | 3  | 0  | 4  | 1,00      | 0,43   | 0,60     |
| JOBADS2 | 2              | 1  | 0  | 1  | 1,00      | 0,50   | 0.67     |
| JOBADS3 | 3              | 1  | 0  | 2  | 1,00      | 0,33   | 0,50     |
| JOBADS4 | 2              | 1  | 1  | 1  | 1,00      | 0,50   | 0,67     |
| JOBADS5 | 3              | 0  | 1  | 3  | 0,00      | 0,00   | 0,00     |
| **Total** |              |    |    |    | **0,80**  | **0,35** | **0,49** |

https://github.com/AnonymousResearcher15/GenderBiasRadar.git
