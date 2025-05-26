from pyswip import Prolog
import yaml
import os

class Adapter:
    def __init__(self, prologRules, prologFile, prologFacts, prologConstraints, constraints, explanationFile, yamlOut, infrastructure, energyMix):
        self.prologRules = prologRules
        self.prologFile = prologFile
        self.prologFacts = prologFacts
        self.constraints = constraints
        self.prologConstraints = prologConstraints
        self.explanationFile = explanationFile
        self.yamlout = yamlOut
        self.infrastructure = infrastructure
        self.energyMix = energyMix

    # Create the prolog file and execute it
    def adapt_output(self):
        """Adapts to the correct format the output."""
        def explain(constrType):
            match constrType:
                case "affinity":
                    return "since the services exchanged a lot of data between them"
                case "avoidNode":
                    return "This decision was driven by the high resource consumption of the selected flavour combined with the poor energy mix of the target node."

        def savings(constraint):
            def obtainIndex(data, element):
                index = next(i for i, item in enumerate(data) if item["node"] == element)
                return index
            nodes = []
            minNode = min(self.infrastructure["nodes"], key=lambda x: self.energyMix.gather_energyMix(x))
            for node in self.infrastructure["nodes"]:
                details = {"node": node,
                           "carbon": self.infrastructure["nodes"][node]["profile"]["carbon"]}
                nodes.append(details)
            nodes = sorted(nodes, key=lambda x: x['carbon'], reverse=True)
            index = min(obtainIndex(nodes, constraint["node"]), len(nodes))
            maxSave = constraint["constraint_emissions"] - (constraint["constraint_emissions"] / nodes[index]["carbon"] * self.infrastructure["nodes"][minNode]["profile"]["carbon"])
            minSave = constraint["constraint_emissions"] - (constraint["constraint_emissions"] / nodes[index]["carbon"] * nodes[index+1]["carbon"])
            return f"The estimated emissions savings resulting from avoiding this deployment range between {maxSave} gCO2eq and {minSave} gCO2eq."

        with open(self.prologFile, 'w') as file:
            for fact in self.prologFacts:
                file.write(fact + ".\n")

        Prolog().consult("rules.pl")

        maxV = max(x["constraint_emissions"] for x in self.constraints)
        
        with open(self.explanationFile, "w") as explfile:
            for constraint in self.constraints:
                if (constraint.get("constraint_emissions") / maxV) > 0.3:
                    if constraint["category"] == "affinity":
                        explanation = (f'A {constraint["category"]} was generated '
                            f'between {constraint["source"]} in flavour {constraint["source_flavour"]} '
                            f'and {constraint["destination"]} in flavour {constraint["destination_flavour"]} '
                            f'{explain(constraint["category"])}\n')
                        explfile.write(explanation)
                    elif constraint["category"] == "avoid":
                        constraint["category"] = "avoidNode"
                        explanation = (f'A {constraint["category"]} constraint was generated '
                            f'for the deployment of the {constraint["source"]} component in the {constraint["flavour"]} flavour '
                            f'on the {constraint["node"]} node. {explain(constraint["category"])}\n'
                            f'{savings(constraint)}\n'
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
                affinityvalue = element.get("destination", "") #+ "," + element.get("destination_flavour", "")
                
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