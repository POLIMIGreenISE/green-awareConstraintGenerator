import json
import math
import yaml
from pyswip import Prolog

# When constrainst should stop being produced
knowledgeBaseMemoryThreshold = 0.5

def handleKnowledgeBase(knowledgeBase, istio, kepler, constraints, rules):
    with open(knowledgeBase, "r") as file:
        myKnowledgeBase = yaml.safe_load(file)
    
    def sigmoid_decay_step(weight):
        k = 2
        multiplier = 1 / (1 + math.exp(k * (1 - weight)))
        new_weight = weight * multiplier
        return new_weight

    if not myKnowledgeBase:
        # We have no previous knowledge, save the basis
        services = []
        connections = []
        constr = []
        for element in kepler:
            pastData = {
                "emissions": element["emissions"],
                "joules": element["joules"],
                "count": 1
            }
            historyData = {
                "service": element["service"],
                "history": pastData
            }
            services.append(historyData)
        for element in istio:
            pastData = {
                "emissions": element["emissions"],
                "joules": element["joules"],
                "count": 1
            }
            historyData = {
                "source": element["source"],
                "destination": element["destination"],
                "history": pastData
            }
            connections.append(historyData)
        for element in constraints:
            element["weight"] = 1.0
            constr.append(element)
        knowledge = {
            "services": services,
            "connections": connections,
            "constraints": constr
        }

        with open(knowledgeBase, "w") as json_file:
            json.dump(knowledge, json_file, indent=4)
    else:
        for element in kepler:
            service_found = False
            for service in myKnowledgeBase["services"]:
                if service["service"] == element["service"]:
                    service["history"]["emissions"] += element["emissions"]
                    service["history"]["joules"] += element["joules"]
                    service["history"]["count"] += 1
                    service["history"]["emissions"] /= service["history"]["count"]
                    service["history"]["joules"] /= service["history"]["count"]
                    service_found = True
                    break
            if not service_found:
                newKnowledge = {
                    "service": element["service"],
                    "history":
                        {
                            "emissions": element["emissions"],
                            "joules": element["joules"],
                            "count": 1
                        }
                }
                myKnowledgeBase["services"].append(newKnowledge) 
        for element in istio:
            pairing_found = False
            for connection in myKnowledgeBase["connections"]:
                if connection["source"] == element["source"] and connection["destination"] == element["destination"]:
                    service["history"]["emissions"] += element["emissions"]
                    service["history"]["joules"] += element["joules"]
                    service["history"]["count"] += 1
                    service["history"]["emissions"] /= service["history"]["count"]
                    service["history"]["joules"] /= service["history"]["count"]
                    pairing_found = True
                    break
            if not pairing_found:
                newKnowledge = {
                    "source": element["service"],
                    "destination": element["destination"],
                    "history": 
                        {
                            "emissions": element["emissions"],
                            "joules": element["joules"],
                            "count": 1
                        }
                }
                myKnowledgeBase["connections"].append(newKnowledge)
        for element in constraints:
            constr_found = False
            for constr in myKnowledgeBase["constraints"]:
                if constr["source"] == element["source"] and constr["source_flavour"] == element['source_flavour'] \
                    and constr["destination"] == element["destination"] and constr["destination_flavour"] == element['destination_flavour']:
                    constr_found = True
                    break
            if not constr_found:
                myKnowledgeBase["constraints"].append(element)
        for constr in myKnowledgeBase["constraints"]:
            constr_found = False
            for element in constraints:
                if constr["source"] == element["source"] and constr["source_flavour"] == element['source_flavour'] \
                    and constr["destination"] == element["destination"] and constr["destination_flavour"] == element['destination_flavour']:
                    constr_found = True
                    break
            if not constr_found:
                constr["weight"] = sigmoid_decay_step(constr["weight"])

        with open(knowledgeBase, "w") as json_file:
            json.dump(myKnowledgeBase, json_file, indent=4)    

    if myKnowledgeBase is not None:
        for element in myKnowledgeBase["constraints"]:
            if knowledgeBaseMemoryThreshold < element["weight"] < 1.0:
                new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_weight"]})"
                rules.append(new_rule)
    else:
        for element in knowledge["constraints"]:
            if knowledgeBaseMemoryThreshold < element["weight"] < 1.0:
                new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_weight"]})"
                rules.append(new_rule)
    return rules