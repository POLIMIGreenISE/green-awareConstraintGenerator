class Affinity:
    def __init__(self):
        self.affinityConstraints = []

    def generate_constraints(self, deployment, infrastructure, monitorIstio, energyMix):
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

        # For each communication of interest, save that there is an affinity
        for comm in monitorIstio:
            if set(obtainDeployableNodes(comm['source'],infrastructure)) & set(obtainDeployableNodes(comm['destination'],infrastructure)):
                affinity = {
                    "category": "affinity",
                    "source": comm["source"],
                    "source_flavour": findFlavour(comm['source'], deployment),
                    "destination": comm["destination"],
                    "destination_flavour": findFlavour(comm['destination'], deployment),
                    "constraint_emissions": comm['emissions'] * (energyMix.gather_energyMix(findNode(comm["source"], deployment)) + energyMix.gather_energyMix(findNode(comm["destination"],deployment))) / 2
                }
                self.affinityConstraints.append(affinity)

        return self.affinityConstraints
    
    def get_neededThreshold(self):
        return ["istioThreshold"]