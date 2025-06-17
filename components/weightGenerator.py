import json
import re

class WeightGenerator:
    def __init__(self, constraints, prologFacts, deployment):
        self.constraints = constraints
        self.prologFacts = prologFacts
        self.deployment = deployment

    def generate_weights(self):
        """
        Generate the weights of our constraints given an average global gco2e consumtpion if our services consume below
        give them a malus multiplier
        """
        average_global = 100
        multiplier = 0.75
        contraints_threshold = 0.1 

        maxConsumption = max(constr["constraint_emissions"] for constr in self.constraints)
        
        for constr in self.constraints:
            if constr["category"] == "affinity":
                if maxConsumption < average_global:
                    final_weight = constr["constraint_emissions"] * multiplier
                    final_weight /= average_global
                elif constr["constraint_emissions"] < average_global:
                    final_weight = constr["constraint_emissions"] * multiplier
                    final_weight /= maxConsumption
                else:
                    final_weight = constr["constraint_emissions"] / maxConsumption
                new_rule = f"highConsumptionConnection({constr['source']},{constr['source_flavour']},{constr['destination']},{constr['destination_flavour']},{final_weight:.3f})"
                self.prologFacts.append(new_rule)
            elif constr["category"] == "avoid":
                if maxConsumption < average_global:
                    final_weight = constr["constraint_emissions"] * multiplier
                    final_weight /= average_global
                elif constr["constraint_emissions"] < average_global:
                    final_weight = constr["constraint_emissions"] * multiplier
                    final_weight /= maxConsumption
                else:
                    final_weight = constr["constraint_emissions"] / maxConsumption
                new_rule = f"highConsumptionService({constr['source']},{constr['flavour']},{constr['node']},{final_weight:.3f})"
                self.prologFacts.append(new_rule)

        itemsToRemove = []
        for fact in self.prologFacts:
            if fact.startswith("highConsumption"):
                match = re.match(r'(\w+)\((.*?)\)', fact)
                if match:
                    args = match.group(2).split(',')
                    if float(args[-1]) < contraints_threshold:
                        itemsToRemove.append(fact)
        for fact in itemsToRemove:
            self.prologFacts.remove(fact)
        
        return self.prologFacts