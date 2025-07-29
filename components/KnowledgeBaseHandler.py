import json
import math
from datetime import datetime

class KnowledgeBaseHandler:
    def __init__(self, knowledgeBase, istio, kepler, generatedConstraints, infrastructure, energyMix):
        self.knowledgeBase = knowledgeBase
        self.istio = istio
        self.kepler = kepler
        self.generatedConstraints = generatedConstraints
        self.infrastructure = infrastructure
        self.energyMix = energyMix
        self.constraints = None
        
    def handle_knowledgeBase(self):
        """
        Handle the knowledgeBase, which includes historical information about consumptions.
        It stores the following information:
        Services:
        - Service
        - History
            - Timestamp
            - Flavour
            - Emissions (Max/Min/Avg)
        
        Connections:
        - Source
        - Destination
        - History
            - Timestamp
            - Source Flavour
            - Destination Flavour 
            - Emissions (Max/Min/Avg)
        
        Constraints:
        - Timestamp
        - Category
        - Source/Destination depending on the category
        - Emissions
        - Memory Weight
        
        Nodes:
        - Timestamp
        - Node
        - Energy Mix
        """
        # Threshold telling us when self.constraints should stop being remembered
        knowledgeBaseMemoryThreshold = 0.5  
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Open the knowledge base
        try:
            with open(self.knowledgeBase, "r") as file:
                myKnowledgeBase = json.load(file)
        except json.JSONDecodeError:
            myKnowledgeBase = {}
        # Step sigmoid function to handle memory decay
        def sigmoid_decay_step(weight):
            k = 2
            multiplier = 1 / (1 + math.exp(k * (0.15 - weight)))
            new_weight = weight * multiplier
            return new_weight
        # If the knowledge base is empty
        if not myKnowledgeBase:
            # We have no previous knowledge, save the basis
            services = []
            connections = []
            constr = []
            nodes = []
            # Save each kepler element
            for element in self.kepler:
                pastData = {
                    "timestamp": timestamp,
                    "flavour": element["flavour"],
                    "emissions": element["emissions"],
                    "max_emissions": element["emissions"],
                    "min_emissions": element["emissions"],
                    "joules": element["joules"],
                    "count": 1
                }
                historyData = {
                    "service": element["service"],
                    "history": [pastData]
                }
                services.append(historyData)
            # Save each istio element
            for element in self.istio:
                pastData = {
                    "timestamp": timestamp,
                    "source_flavour": element["source_flavour"],
                    "destination_flavour": element["destination_flavour"],
                    "emissions": element["emissions"],
                    "max_emissions": element["emissions"],
                    "min_emissions": element["emissions"],
                    "joules": element["joules"],
                    "count": 1
                }
                historyData = {
                    "source": element["source"],
                    "destination": element["destination"],
                    "history": [pastData]
                }
                connections.append(historyData)
            # Save each constraint produced so far, and give a memory weight of 1
            for element in self.generatedConstraints:
                element["memory_weight"] = 1.0
                element["timestamp"] = timestamp
                constr.append(element)
            for element in self.infrastructure["nodes"]:
                node = {
                    "timestamp": timestamp,
                    "node": element,
                    "mix":  self.energyMix.gather_energyMix(element)
                }
                nodes.append(node)
            knowledge = {
                "services": services,
                "connections": connections,
                "constraints": constr,
                "nodes": nodes
            }
            # Save the knowledge aquired
            with open(self.knowledgeBase, "w") as json_file:
                json.dump(knowledge, json_file, indent=4)
        # If our knowledge base is not empty
        else:
            # For each kepler element
            for element in self.kepler:
                service_found = False
                flavour_found = False
                # If the service already existed, update the service average
                for service in myKnowledgeBase["services"]:
                    if service["service"] == element["service"]:
                        for historyPoint in service["history"]:
                            if historyPoint["flavour"] == element["flavour"]:
                                historyPoint["timestamp"] = timestamp
                                historyPoint["emissions"] += element["emissions"]
                                historyPoint["joules"] += element["joules"]
                                historyPoint["count"] += 1
                                if element["emissions"] > historyPoint["max_emissions"]:
                                    historyPoint["max_emissions"] = element["emissions"]
                                if element["emissions"] < historyPoint["min_emissions"]:
                                    historyPoint["min_emissions"] = element["emissions"]
                                flavour_found = True
                                break
                        # Otherwise add the flavour
                        if not flavour_found:
                            newFlavour = {
                                "timestamp": timestamp,
                                "flavour": element["flavour"],
                                "emissions": element["emissions"],
                                "max_emissions": element["emissions"],
                                "min_emissions": element["emissions"],
                                "joules": element["joules"],
                                "count": 1   
                            }
                            service["history"].append(newFlavour)
                        service_found = True
                        break
                # Otherwise add the service
                if not service_found:
                    newKnowledge = {
                        "service": element["service"],
                        "history": [
                            {
                                "timestamp": timestamp,
                                "flavour": element["flavour"],
                                "emissions": element["emissions"],
                                "max_emissions": element["emissions"],
                                "min_emissions": element["emissions"],
                                "joules": element["joules"],
                                "count": 1
                            }
                        ]
                    }
                    myKnowledgeBase["services"].append(newKnowledge)
            # For each istio element
            for element in self.istio:
                pairing_found = False
                pairing_flavours = False
                # If the connection already existed, update the connection average
                for connection in myKnowledgeBase["connections"]:
                    if connection["source"] == element["source"] and connection["destination"] == element["destination"]:
                        for historyPoint in connection["history"]:
                            if historyPoint["source_flavour"] == element["source_flavour"] and \
                            historyPoint["destination_flavour"] == element["destination_flavour"]:
                                historyPoint["timestamp"] = timestamp
                                historyPoint["emissions"] += element["emissions"]
                                historyPoint["joules"] += element["joules"]
                                historyPoint["count"] += 1
                                if element["emissions"] > historyPoint["max_emissions"]:
                                    historyPoint["max_emissions"] = element["emissions"]
                                if element["emissions"] < historyPoint["min_emissions"]:
                                    historyPoint["min_emissions"] = element["emissions"]
                                pairing_flavours = True
                                break
                        # Otherwise add the flavour
                        if not pairing_flavours:
                            newFlavourPair = {
                                "timestamp": timestamp,
                                "source_flavour": element["source_flavour"],
                                "destination_flavour": element["destination_flavour"],
                                "emissions": element["emissions"],
                                "max_emissions": element["emissions"],
                                "min_emissions": element["emissions"],
                                "joules": element["joules"],
                                "count": 1                         
                            }
                            connection["history"].append(newFlavourPair)
                        pairing_found = True
                        break
                # Otherwise add the connection
                if not pairing_found:
                    newKnowledge = {
                        "source": element["service"],
                        "destination": element["destination"],
                        "history": [
                            {
                                "timestamp": timestamp,
                                "source_flavour": element["source_flavour"],
                                "destination_flavour": element["destination_flavour"],
                                "emissions": element["emissions"],
                                "max_emissions": element["emissions"],
                                "min_emissions": element["emissions"],
                                "joules": element["joules"],
                                "count": 1
                            }
                        ]
                    }
                    myKnowledgeBase["connections"].append(newKnowledge)
            # For each constraint
            excluded_keys = {"constraint_emissions", "memory_weight", "timestamp"}
            for element in self.generatedConstraints:
                constr_found = False
                # If the constraint already existed, update its consumption
                for constr in myKnowledgeBase["constraints"]:
                    shared_keys = set(constr.keys()) & set(element.keys()) - excluded_keys
                    if all(constr.get(k) == element.get(k) for k in shared_keys):
                        constr_found = True
                        constr["constraint_emissions"] = element["constraint_emissions"]
                        constr["timestamp"] = timestamp
                        break
                # Otherwise add it
                if not constr_found and constr["category"]:
                    element["memory_weight"] = 1.0
                    element["timestamp"] = timestamp
                    myKnowledgeBase["constraints"].append(element)
            # Now we search all the self.constraints that were not among our current self.constraints, and update their memory weight
            for constr in myKnowledgeBase["constraints"]:
                constr_found = False
                for element in self.generatedConstraints:
                    shared_keys = set(constr.keys()) & set(element.keys()) - excluded_keys
                    if all(constr.get(k) == element.get(k) for k in shared_keys):
                        constr_found = True
                        constr["memory_weight"] = 1.0
                        break
                if not constr_found and constr["category"]:
                    constr["memory_weight"] = sigmoid_decay_step(constr["memory_weight"])
            for element in self.infrastructure["nodes"]:
                node_found = False
                for node in myKnowledgeBase["nodes"]:
                    if element == node["node"]:
                        node_found = True
                        node["timestamp"] = timestamp
                        node["mix"] = self.energyMix.gather_energyMix(element)
                        break
                if not node_found:
                    newNode = {
                        "timestamp": timestamp,
                        "node": element,
                        "mix": self.energyMix.gather_energyMix(element)
                    }
                    myKnowledgeBase["nodes"].append(newNode)
            # Save the knowledge base
            with open(self.knowledgeBase, "w") as json_file:
                json.dump(myKnowledgeBase, json_file, indent=4)    

        self.constraints = []
        # Save all the rules that need to be passed to the weightGenerator
        if myKnowledgeBase:
            for element in myKnowledgeBase["constraints"]:
                if knowledgeBaseMemoryThreshold < element["memory_weight"] <= 1.0:
                    #new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_emissions"]})"
                    self.constraints.append(element)
                    #rules.append(new_rule)
        else:
            for element in knowledge["constraints"]:
                if knowledgeBaseMemoryThreshold < element["memory_weight"] <= 1.0:
                    #new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_emissions"]})"
                    self.constraints.append(element)
                    #rules.append(new_rule)

        return self.constraints