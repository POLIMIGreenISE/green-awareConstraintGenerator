import json
import yaml
import statistics

class ConstraintsGenerator:
    def __init__(self, istio, kepler, deployment, infrastructure, application, knowledgeBase, energyMix):
        self.istio = istio
        self.kepler = kepler
        self.deployment = deployment
        self.infrastructure = infrastructure
        self.application = application
        self.knowledgeBase = knowledgeBase
        self.energyMix = energyMix
        self.affinity = None
        self.avoid = None
        self.maxConsumption = None
        self.prologFacts = None
        with open(self.application, "r") as file:
            self.myapp = yaml.safe_load(file)
    
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

        # Given a service, obtain the nodes that match its resources
        def obtainResourcefulNodes(service, infrastructure):
            resourcefulNodes = []
            mysecurity = self.myapp["requirements"]["components"][service["service"]]["common"]["security"]
            mycpu = self.myapp["requirements"]["components"][service["service"]]["flavour-specific"][service["flavour"]]["cpu"]
            myram = self.myapp["requirements"]["components"][service["service"]]["flavour-specific"][service["flavour"]]["ram"]
            isDeployable = True
            for node in infrastructure["nodes"]:
                for property in infrastructure["nodes"][node]["capabilities"]:
                    if property == "security":
                        if set(mysecurity) & set(infrastructure["nodes"][node]["capabilities"][property]):
                            isDeployable = True
                        else:
                            isDeployable = False
                    if property == "cpu":
                        if mycpu > infrastructure["nodes"][node]["capabilities"][property]:
                            isDeployable = False
                    if property == "ram":
                        if myram > infrastructure["nodes"][node]["capabilities"][property]:
                            isDeployable = False
                if isDeployable:
                    resourcefulNodes.append(node)
            return resourcefulNodes

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
        #maxNode = max(self.infrastructure["nodes"], key=lambda x: self.energyMix.gather_energyMix(x))

        # Dynamic Thresholding
        cut_points = 5
        threshold_points = 3
        if not myKnowledgeBase:
            # Findthe avg consumption for all our estimates
            istioThreshold = statistics.quantiles([x["emissions"] for x in self.istio], n=cut_points)[threshold_points]
            # 75th quantile
            keplerThreshold = statistics.quantiles([x["emissions"] for x in self.kepler], n=cut_points)[threshold_points]
        else:
            quant_istio = []
            for element in myKnowledgeBase["connections"]:
                for historyPoint in element["history"]:
                    quant_istio.append((historyPoint["emissions"] / historyPoint["count"]))
            for element in self.istio:
                quant_istio.append(element["emissions"])
            istioThreshold = statistics.quantiles(quant_istio, n=cut_points)[threshold_points]
            # 75th quantile
            quant_kepler = []
            for element in myKnowledgeBase["services"]:
                for historyPoint in element["history"]:
                    quant_kepler.append((historyPoint["emissions"] / historyPoint["count"]))
            for element in self.kepler:
                quant_kepler.append(element["emissions"])
            keplerThreshold = statistics.quantiles(quant_kepler, n=cut_points)[threshold_points]
        # Filter only the consumption above the threshold, which are to our interest
        monitorIstio = checkThreshold(self.istio, 'emissions', istioThreshold)
        monitorIstio = sorted(monitorIstio, key=lambda x: x['emissions'], reverse=True)
        monitorKepler = checkThreshold(self.kepler, 'emissions', keplerThreshold)
        monitorKepler = sorted(monitorKepler, key=lambda x: x['emissions'], reverse=True)      
        
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
                    "constraint_emissions": comm['emissions'] * (self.energyMix.gather_energyMix(findNode(comm["source"], self.deployment)) + self.energyMix.gather_energyMix(findNode(comm["destination"], self.deployment))) / 2
                }
                self.affinity.append(affinity)

        # For each service of interest, save that there is an avoid
        for service in monitorKepler:
            serviceWeight = float(service['emissions'])
            deployableNodes = obtainDeployableNodes(service["service"], self.infrastructure)
            resourcefulNodes = obtainResourcefulNodes(service, self.infrastructure)
            considerableNodes = set(deployableNodes) & set(resourcefulNodes)
            maxDeployable = max(considerableNodes)
            if len(considerableNodes) > 1:
                for node in considerableNodes:
                    nodeWeight = float(self.energyMix.gather_energyMix(node) / self.energyMix.gather_energyMix(maxDeployable))
                    scaledWeight = nodeWeight * serviceWeight
                    if(scaledWeight >= keplerThreshold):
                        avoid = {
                            "category": "avoid",
                            "source": service["service"],
                            "flavour": findFlavour(service['service'], self.deployment),
                            "node": node,
                            "constraint_emissions": service["emissions"] * self.energyMix.gather_energyMix(node)
                        }
                        self.avoid.append(avoid)

        # Avoid scenarios where a service is told to avoid all its deployable nodes
        seen_sources = set()
        itemsToRemove = []
        for avoid in self.avoid:
            source = avoid["source"]
            if source not in seen_sources:
                avoidInstances = sum(1 for item in self.avoid if item.get("source") == source)
                seen_sources.add(source)
                myservice = {
                    "service": source,
                    "flavour": avoid["flavour"]
                }
                availableNodes = set(obtainResourcefulNodes(myservice, self.infrastructure)) & set(obtainDeployableNodes(myservice["service"], self.infrastructure))
                if avoidInstances == len(availableNodes):
                    pendingRemoval = min((item for item in self.avoid if item["source"] == source), key=lambda x: x["constraint_emissions"], default=None)
                    itemsToRemove.append(pendingRemoval)

        for removed in itemsToRemove:
            self.avoid.remove(removed)

        return self.affinity, self.avoid, self.maxConsumption, self.prologFacts