import json
import statistics
from .energyMixGatherer import gatherEnergyMix

# From the metrics, sorted from highest consumption to lowest, obtain the constraints to produce in output
def generateConstraints(finalIstio, finalKepler, deploymentinfo, myInfrastructure, knowledgeBase, energyMix):

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
   
    with open(energyMix, "r") as file:
        myEnergyMix = json.load(file)

    # Open knowledgebase
    try:
        with open(knowledgeBase, "r") as file:
            myKnowledgeBase = json.load(file)
    except json.JSONDecodeError:
        myKnowledgeBase = {}

    # Find the max consumption for all our estimates
    maxIstio = max(finalIstio, key=lambda x: x['emissions'])
    maxKepler = max(finalKepler, key=lambda x: x['emissions'])
    maxAll = max(maxIstio['emissions'], maxKepler['emissions'])
    maxNode = max(myEnergyMix, key=lambda x: gatherEnergyMix(myEnergyMix, x))

    # Dynamic Thresholding
    if not myKnowledgeBase:
        # Findthe avg consumption for all our estimates
        istioThreshold = statistics.mean(x["emissions"] for x in finalIstio)
        # 75th quantile
        keplerThreshold = statistics.quantiles([x["emissions"] for x in finalKepler], n=4)[2]
    else:
        cumsum = 0
        for element in myKnowledgeBase["connections"]:
            cumsum += element["history"]["emissions"] / element["history"]["count"]
        for element in finalIstio:
            cumsum += element["emissions"]
        # Findthe avg consumption for all our estimates
        istioThreshold = cumsum / (len(myKnowledgeBase["services"]) + len(finalIstio))
        # 75th quantile
        quant = []
        for element in myKnowledgeBase["services"]:
            quant.append((element["history"]["emissions"] / element["history"]["count"]))
        for element in finalKepler:
            quant.append(element["emissions"])
        keplerThreshold = statistics.quantiles(quant, n=4)[2]

    # Filer only the consumption above the threshold, which are to our interest
    monitorIstio = checkThreshold(finalIstio, 'emissions', istioThreshold)
    monitorIstio = sorted(monitorIstio, key=lambda x: x['emissions'], reverse=True)
    monitorKepler = checkThreshold(finalKepler, 'emissions', keplerThreshold)          
    
    prologFacts = []
    affinityConstraints = []
    avoidConstraints = []

    # Prolog file preparation
    # For each communication in our Istio metrics, save the fact
    for comm in finalIstio:
        fact = f"serviceConnection({comm["source"]}, {comm["destination"]}, {comm["emissions"]}, {comm["joules"]})"
        prologFacts.append(fact)
    # For each service in our Kepler metrics, save the fact    
    for service in finalKepler:
        fact = f"service({service["service"]}, {service["emissions"]}, {service["joules"]})"
        prologFacts.append(fact)
    # For each node in our infrastructure, save the fact
    for node in myInfrastructure:
        fact = f"node({node}, {myInfrastructure[node]["profile"]["carbon"]})"
        prologFacts.append(fact)
    # For each element in our deployment, save the fact
    for element in deploymentinfo:
        rule = f"deployedTo({element["service"]},{element["flavour"]},{element["node"]})"
        prologFacts.append(rule)

    # For each communication of interest, save that there is an affinity
    for comm in monitorIstio:
        affinity = {
            "category": "affinity",
            "source": comm["source"],
            "source_flavour": findFlavour(comm['source'], deploymentinfo),
            "destination": comm["destination"],
            "destination_flavour": findFlavour(comm['destination'], deploymentinfo),
            "constraint_emissions": comm['emissions']
        }
        affinityConstraints.append(affinity)

    # For each service of interest, save that there is an avoid
    for service in monitorKepler:
        serviceWeight = float(service['emissions'])
        for node in myInfrastructure:
            nodeWeight = float(gatherEnergyMix(myEnergyMix, node) / gatherEnergyMix(myEnergyMix, maxNode))
            scaledWeight = nodeWeight * serviceWeight
            if(scaledWeight >= keplerThreshold):
                avoid = {
                    "category": "avoid",
                    "source": service["service"],
                    "flavour": findFlavour(service['service'], deploymentinfo),
                    "node": node,
                    "constraint_emissions": service["emissions"]
                }
                avoidConstraints.append(avoid)
 
    return affinityConstraints, avoidConstraints, maxAll, prologFacts