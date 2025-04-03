import json
from components.EnergyMixGatherer import EnergyMixGatherer

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

        def findNode(service, services):
            for s in services:
                if s["service"] == service:
                    return s["node"]

        for constr in self.constraints:
            constr["constraint_emissions"] *= EnergyMixGatherer(findNode(constr["source"], self.deployment)).gather_energyMix()

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
                new_rule = f"highConsumptionConnection({constr['source']},{constr["source_flavour"]},{constr['destination']},{constr["destination_flavour"]},{final_weight:.3f})"
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
                new_rule = f"highConsumptionService({constr["source"]},{constr["flavour"]},{constr["node"]},{final_weight:.3f})"
                self.prologFacts.append(new_rule)

        return self.prologFacts