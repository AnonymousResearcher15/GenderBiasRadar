from collections import defaultdict
import random


class CustomRAG:
  def __init__(self, dataset):
    self.dataset = dataset
    self.examples_by_rule = defaultdict(list)
    self.preprocess_dataset()


  def preprocess_dataset(self):
    """Pre-process the dataset to organize examples by rule_id"""
    for example in self.dataset:
      self.examples_by_rule[example["rule_id"]].append(example)


  def retrieve_examples(self, n_per_rule=1):
    """Retrieve examples from the dataset based on the defined rules"""
    retrieve_examples = self.get_examples_for_all_rules(n_per_rule)
    return self.structured_dataset(retrieve_examples)

  def get_examples_for_all_rules(self, n_per_rule=1):
    """Get n examples from each of the 9 rules"""
    retrieved = {}
    for rule_id in range(1, 10):  # Rules 1-9
        if rule_id in self.examples_by_rule:
            # Sample n examples (or fewer if not enough exist)
            retrieved[rule_id] = random.sample(
                self.examples_by_rule[rule_id], 
                min(n_per_rule, len(self.examples_by_rule[rule_id]))
            )
    return retrieved


  def structured_dataset(self, retrieved_examples):
    """Convert the retrieved examples into a structured format"""
    structured_text = ""
    example = 1
    for rule_id, ex_list in retrieved_examples.items():
      for ex in ex_list:
        structured_text += f"ΠΑΡΑΔΕΙΓΜΑ {example}:\n"
        structured_text += f"ΚΕΙΜΕΝΟ: {ex['biased_text']}\n"
        if ex.get('entities'):
          structured_text += "ΟΝΤΟΤΗΤΕΣ:\n"
          for entity in ex['entities']:
            structured_text += f"-{entity}\n"
        structured_text += f"ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: {ex['mitigated_text']}\n"
        example += 1
    return structured_text

# ΠΑΡΑΔΕΙΓΜΑ 1 (άγνωστος ρόλος, παρότι είναι ήδη θηλυκό στο κείμενο)
# ΚΕΙΜΕΝΟ: γιατί κωλύεται η Εισαγγελέας
# ΟΝΤΟΤΗΤΕΣ:
# - Γραμματέας -> Αικατερίνη Σιταρά, θηλυκό
# - Δικαστής -> Γεώργιος Σακκάς, αρσενικό
# ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: γιατί κωλύεται ο/η Εισαγγελέας