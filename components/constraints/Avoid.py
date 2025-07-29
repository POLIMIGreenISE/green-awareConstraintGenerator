class Avoid:
    def __init__(self):
        self.avoidConstraints = []

    def generate_constraints(self, deployment, infrastructure, myapp, maxThreshold, monitorKepler, energyMix):
        # Given a service find which node it was deployed on
        def findNode(service, services):
            for s in services:
                if s["service"] == service:
                    return s["node"]

        # Given a service find which flavour it was deployed as
        def findFlavour(service, services):
            for s in services:
                if s["service"] == service:
                    return s["flavour"]

        # Given a service, obtain only the deployable nodes
        def obtainDeployableNodes(service, infrastructure):
            deployableNodes = []
            mynode = findNode(service, deployment)
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
            mysecurity = myapp["requirements"]["components"][service["service"]]["common"]["security"]
            mycpu = myapp["requirements"]["components"][service["service"]]["flavour-specific"][service["flavour"]]["cpu"]
            myram = myapp["requirements"]["components"][service["service"]]["flavour-specific"][service["flavour"]]["ram"]
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

        # For each service of interest, save that there is an avoid
        for service in monitorKepler:
            serviceWeight = float(service['emissions'])
            deployableNodes = obtainDeployableNodes(service["service"], infrastructure)
            resourcefulNodes = obtainResourcefulNodes(service, infrastructure)
            considerableNodes = set(deployableNodes) & set(resourcefulNodes)
            maxDeployable = max(considerableNodes)
            if len(considerableNodes) > 1:
                for node in considerableNodes:
                    nodeWeight = float(energyMix.gather_energyMix(node) / energyMix.gather_energyMix(maxDeployable))
                    scaledWeight = nodeWeight * serviceWeight
                    if(scaledWeight >= maxThreshold):
                        avoid = {
                            "category": "avoid",
                            "source": service["service"],
                            "flavour": findFlavour(service['service'], deployment),
                            "node": node,
                            "constraint_emissions": service["emissions"] * energyMix.gather_energyMix(node)
                        }
                        self.avoidConstraints.append(avoid)

        # Avoid scenarios where a service is told to avoid all its deployable nodes
        seen_sources = set()
        itemsToRemove = []
        for avoid in self.avoidConstraints:
            source = avoid["source"]
            if source not in seen_sources:
                avoidInstances = sum(1 for item in self.avoidConstraints if item.get("source") == source)
                seen_sources.add(source)
                myservice = {
                    "service": source,
                    "flavour": avoid["flavour"]
                }
                availableNodes = set(obtainResourcefulNodes(myservice, infrastructure)) & set(obtainDeployableNodes(myservice["service"], infrastructure))
                if avoidInstances == len(availableNodes):
                    pendingRemoval = min((item for item in self.avoidConstraints if item["source"] == source), key=lambda x: x["constraint_emissions"], default=None)
                    itemsToRemove.append(pendingRemoval)

        for removed in itemsToRemove:
            self.avoidConstraints.remove(removed)

        return self.avoidConstraints
    
    def get_neededThreshold(self):
        return ["keplerThreshold"]