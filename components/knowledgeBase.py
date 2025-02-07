import json
import math
import yaml
from pyswip import Prolog

# Threshold telling us when constraints should stop being remembered
knowledgeBaseMemoryThreshold = 0.5

def handleKnowledgeBase(knowledgeBase, istio, kepler, constraints):
    # Open the knowledge base
    with open(knowledgeBase, "r") as file:
        myKnowledgeBase = yaml.safe_load(file)
    
    # Step sigmoid function to handle memory decay
    def sigmoid_decay_step(weight):
        k = 2
        multiplier = 1 / (1 + math.exp(k * (1 - weight)))
        new_weight = weight * multiplier
        return new_weight

    # If the knowledge base is empty
    if not myKnowledgeBase:
        # We have no previous knowledge, save the basis
        services = []
        connections = []
        constr = []
        # Save each kepler element
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
        # Save each istio element
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
        # Save each constraint produced so far, and give a memory weight of 1
        for element in constraints:
            element["memory_weight"] = 1.0
            constr.append(element)
        knowledge = {
            "services": services,
            "connections": connections,
            "constraints": constr
        }
        # Save the knowledge aquired
        with open(knowledgeBase, "w") as json_file:
            json.dump(knowledge, json_file, indent=4)

    # If our knowledge base is not empty
    else:
        # For each kepler element
        for element in kepler:
            service_found = False
            # If the service already existed, update the service average
            for service in myKnowledgeBase["services"]:
                if service["service"] == element["service"]:
                    service["history"]["emissions"] += element["emissions"]
                    service["history"]["joules"] += element["joules"]
                    service["history"]["count"] += 1
                    service["history"]["emissions"] /= service["history"]["count"]
                    service["history"]["joules"] /= service["history"]["count"]
                    service_found = True
                    break
            # Otherwise add it
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
        # For each istio element
        for element in istio:
            pairing_found = False
            # If the connection already existed, update the connection average
            for connection in myKnowledgeBase["connections"]:
                if connection["source"] == element["source"] and connection["destination"] == element["destination"]:
                    service["history"]["emissions"] += element["emissions"]
                    service["history"]["joules"] += element["joules"]
                    service["history"]["count"] += 1
                    service["history"]["emissions"] /= service["history"]["count"]
                    service["history"]["joules"] /= service["history"]["count"]
                    pairing_found = True
                    break
            # Otherwise add it
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
        # For each constraint
        for element in constraints:
            constr_found = False
            # If the constraint already existed, do nothing
            for constr in myKnowledgeBase["constraints"]:
                if constr["source"] == element["source"] and constr["source_flavour"] == element['source_flavour'] \
                    and constr["destination"] == element["destination"] and constr["destination_flavour"] == element['destination_flavour']:
                    constr_found = True
                    break
            # Otherwise add it
            if not constr_found:
                myKnowledgeBase["constraints"].append(element)

        # Now we search all the constraints that were not among our current constraints, and update their memory weight
        for constr in myKnowledgeBase["constraints"]:
            constr_found = False
            for element in constraints:
                if constr["source"] == element["source"] and constr["source_flavour"] == element['source_flavour'] \
                    and constr["destination"] == element["destination"] and constr["destination_flavour"] == element['destination_flavour']:
                    constr_found = True
                    break
            if not constr_found:
                constr["memory_weight"] = sigmoid_decay_step(constr["memory_weight"])

        # Save the knowledge base
        with open(knowledgeBase, "w") as json_file:
            json.dump(myKnowledgeBase, json_file, indent=4)    

    # Save all the rules that need to be passed to the weightGenerator
    if myKnowledgeBase is not None:
        for element in myKnowledgeBase["constraints"]:
            if knowledgeBaseMemoryThreshold < element["memory_weight"] < 1.0:
                #new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_emissions"]})"
                constraints.append(element)
                #rules.append(new_rule)
    else:
        for element in knowledge["constraints"]:
            if knowledgeBaseMemoryThreshold < element["memory_weight"] < 1.0:
                #new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_emissions"]})"
                constraints.append(element)
                #rules.append(new_rule)
    return constraints