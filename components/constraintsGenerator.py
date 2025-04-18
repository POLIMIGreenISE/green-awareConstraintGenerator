import json
import statistics
from components.EnergyMixGatherer import EnergyMixGatherer

class ConstraintsGenerator:
    def __init__(self, istio, kepler, deployment, infrastructure, knowledgeBase):
        self.istio = istio
        self.kepler = kepler
        self.deployment = deployment
        self.infrastructure = infrastructure
        self.knowledgeBase = knowledgeBase
        self.affinity = None
        self.avoid = None
        self.maxConsumption = None
        self.prologFacts = None
    
    def generate_constraints(self):
        """From the metrics, sorted from highest consumption to lowest, obtain the constraints to produce in output."""
        
        # Threshold comparator helper function
        def checkThreshold(array, field, threshold):
            output = []
            for var in array:
                if float(var[field] >= threshold):
                    output.append(var)
            return output
        
        # Given a service find which flavour it was deployed as
        def findFlavour(service, services):
            for s in services:
                if s["service"] == service:
                    return s["flavour"]
    
        # Given a service find which node it was deployed on
        def findNode(service, services):
            for s in services:
                if s["service"] == service:
                    return s["node"]

        # Given a service, obtain only the deployable nodes
        def obtainDeployableNodes(service, infrastructure):
            deployableNodes = []
            mynode = findNode(service, self.deployment)
            
            mysubnet = infrastructure["nodes"][mynode]["capabilities"]["subnet"]
            for node in infrastructure["nodes"]:
                for value in infrastructure["nodes"][node]["capabilities"]:
                    if value == "subnet":
                        if set(mysubnet) & set(infrastructure["nodes"][node]["capabilities"][value]):
                            deployableNodes.append(node)
            return deployableNodes

        # Open knowledgebase
        try:
            with open(self.knowledgeBase, "r") as file:
                myKnowledgeBase = json.load(file)
        except json.JSONDecodeError:
            myKnowledgeBase = {}

        # Find the max consumption for all our estimates
        maxIstio = max(self.istio, key=lambda x: x['emissions'])
        maxKepler = max(self.kepler, key=lambda x: x['emissions'])
        self.maxConsumption = max(maxIstio['emissions'], maxKepler['emissions'])
        maxNode = max(self.infrastructure["nodes"], key=lambda x: EnergyMixGatherer(x).gather_energyMix())

        # Dynamic Thresholding
        if not myKnowledgeBase:
            # Findthe avg consumption for all our estimates
            istioThreshold = statistics.mean(x["emissions"] for x in self.istio)
            # 75th quantile
            keplerThreshold = statistics.quantiles([x["emissions"] for x in self.kepler], n=4)[2]
        else:
            cumsum = 0
            for element in myKnowledgeBase["connections"]:
                for historyPoint in element["history"]:
                    cumsum += historyPoint["emissions"] / historyPoint["count"]
            for element in self.istio:
                cumsum += element["emissions"]
            # Findthe avg consumption for all our estimates
            istioThreshold = cumsum / (len(myKnowledgeBase["services"]) + len(self.istio))
            # 75th quantile
            quant = []
            for element in myKnowledgeBase["services"]:
                for historyPoint in element["history"]:
                    quant.append((historyPoint["emissions"] / historyPoint["count"]))
            for element in self.kepler:
                quant.append(element["emissions"])
            keplerThreshold = statistics.quantiles(quant, n=4)[2]

        # Filer only the consumption above the threshold, which are to our interest
        monitorIstio = checkThreshold(self.istio, 'emissions', istioThreshold)
        monitorIstio = sorted(monitorIstio, key=lambda x: x['emissions'], reverse=True)
        monitorKepler = checkThreshold(self.kepler, 'emissions', keplerThreshold)          
        
        self.prologFacts = []
        self.affinity = []
        self.avoid = []

        # Prolog file preparation
        # For each communication in our Istio metrics, save the fact
        for comm in self.istio:
            fact = f'serviceConnection({comm["source"]}, {comm["destination"]}, {comm["emissions"]}, {comm["joules"]})'
            self.prologFacts.append(fact)
        # For each service in our Kepler metrics, save the fact    
        for service in self.kepler:
            fact = f'service({service["service"]}, {service["emissions"]}, {service["joules"]})'
            self.prologFacts.append(fact)
        # For each node in our infrastructure, save the fact
        for node in self.infrastructure["nodes"]:
            fact = f'node({node}, {self.infrastructure["nodes"][node]["profile"]["carbon"]})'
            self.prologFacts.append(fact)
        # For each element in our deployment, save the fact
        for element in self.deployment:
            rule = f'deployedTo({element["service"]},{element["flavour"]},{element["node"]})'
            self.prologFacts.append(rule)

        # For each communication of interest, save that there is an affinity
        for comm in monitorIstio:
            if set(obtainDeployableNodes(comm['source'],self.infrastructure)) & set(obtainDeployableNodes(comm['destination'],self.infrastructure)):
                affinity = {
                    "category": "affinity",
                    "source": comm["source"],
                    "source_flavour": findFlavour(comm['source'], self.deployment),
                    "destination": comm["destination"],
                    "destination_flavour": findFlavour(comm['destination'], self.deployment),
                    "constraint_emissions": comm['emissions'] * (EnergyMixGatherer(findNode(comm["source"], self.deployment)).gather_energyMix() + EnergyMixGatherer(findNode(comm["destination"], self.deployment)).gather_energyMix()) / 2
                }
                self.affinity.append(affinity)

        # For each service of interest, save that there is an avoid
        for service in monitorKepler:
            serviceWeight = float(service['emissions'])
            deployableNodes = obtainDeployableNodes(service["service"], self.infrastructure)
            if len(deployableNodes) > 1:
                for node in deployableNodes:
                    nodeWeight = float(EnergyMixGatherer(node).gather_energyMix() / EnergyMixGatherer(maxNode).gather_energyMix())
                    scaledWeight = nodeWeight * serviceWeight
                    print(scaledWeight, keplerThreshold)
                    if(scaledWeight >= keplerThreshold):
                        avoid = {
                            "category": "avoid",
                            "source": service["service"],
                            "flavour": findFlavour(service['service'], self.deployment),
                            "node": node,
                            "constraint_emissions": service["emissions"] * EnergyMixGatherer(node).gather_energyMix()
                        }
                        self.avoid.append(avoid)

        return self.affinity, self.avoid, self.maxConsumption, self.prologFacts