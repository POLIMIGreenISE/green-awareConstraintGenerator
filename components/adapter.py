from pyswip import Prolog
import yaml
import os

class Adapter:
    def __init__(self, prologRules, prologFile, prologFacts, prologConstraints, constraints, explanationFile, yamlOut):
        self.prologRules = prologRules
        self.prologFile = prologFile
        self.prologFacts = prologFacts
        self.constraints = constraints
        self.prologConstraints = prologConstraints
        self.explanationFile = explanationFile
        self.yamlout = yamlOut

    # Create the prolog file and execute it
    def adapt_output(self):
        """Adapts to the correct format the output."""
        def explain(constrType):
            match constrType:
                case "affinity":
                    return "since the services exchanged a lot of data between them"
                case "avoid":
                    return "since the services used a lot of resources and the node has a poor energy mix"

        with open(self.prologFile, 'w') as file:
            for fact in self.prologFacts:
                file.write(fact + ".\n")

        Prolog().consult("rules.pl")

        maxV = max(x["constraint_emissions"] for x in self.constraints)

        with open(self.explanationFile, "w") as explfile:
            for constraint in self.constraints:
                if (constraint.get("constraint_emissions") / maxV) > 0.3:
                    if constraint["category"] == "affinity":
                        explanation = (f'A constrant of {constraint["category"]} was generated '
                            f'between {constraint["source"]} in flavour {constraint["source_flavour"]} '
                            f'and {constraint["destination"]} in flavour {constraint["destination_flavour"]} '
                            f'{explain(constraint["category"])}\n')
                        explfile.write(explanation)
                    elif constraint["category"] == "avoid":
                        explanation = (f'A constrant of {constraint["category"]} was generated '
                            f'between {constraint["source"]} in flavour {constraint["flavour"]} '
                            f'and {constraint["node"]} {explain(constraint["category"])}\n'
                            )
                        explfile.write(explanation)

        outputdata = {
        "requirements": {
            "components": {}
        }
        }
        for element in self.constraints:
            if (element.get("constraint_emissions") / maxV) > 0.3:
                source = element["source"]
                flavour = element.get("source_flavour", element.get("flavour", None))
                affinityvalue = element.get("destination", "") + "," + element.get("destination_flavour", "")
                
                if source not in outputdata["requirements"]["components"]:
                    outputdata["requirements"]["components"][source] = {}
                if flavour not in outputdata["requirements"]["components"][source]:
                    outputdata["requirements"]["components"][source][flavour] = []

                outputdata["requirements"]["components"][source][flavour].append({
                    element.get("category"): {
                        "energy_oriented": True,
                        "resilience_oriented": False,
                        "soft": True,
                        "value": element.get("node", affinityvalue)
                    }
                })

        with open(self.yamlout, "w") as file:
            yaml.dump(outputdata, file, default_flow_style=False)