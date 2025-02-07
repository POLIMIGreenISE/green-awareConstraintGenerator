# Threshold for service communications
commThreshold = 0.5
volumeThreshold = 0.5

# Threshold for services joule consumption
serviceThreshold = 0.8

# From the metrics, sorted from highest consumption to lowest, obtain the constraints to produce in output
def generateConstraints(finalIstio, finalKepler, deploymentinfo, myInfrastructure):

    # Threshold comparator helper function
    def checkThreshold(array, field, max, threshold):
        output = []
        for var in array:
            if float(var[field] > (max * threshold)):
                output.append(var)
        return output
    
    # Given a service find which flavour it was deployed as
    def findFlavour(service, services):
        for s in services:
            if s["service"] == service:
                return s["flavour"]

    # Print the total Emissions and the saved Emissions. OUTDATED
    def produceSavingsOut():
        print("Initial Consumption:")
        print("gCO2/h:", totalEmissionsConsumption, "Joules/h:", totalJoulesConsumption)
        print("After applying constraints:")
        postEmissions = totalEmissionsConsumption - totalEmissionsSaved
        postJoules = totalJoulesConsumption - totalJoulesSaved
        print("gCO2/h:", postEmissions, "Joules/h:", postJoules)
        print("Risparmio minimo:", f"{(totalEmissionsConsumption - postEmissions) / totalEmissionsConsumption * 100:.0f}%", 
            "\ngCO2/h risparmiata:", totalEmissionsConsumption - postEmissions, 
            "\nJoules/h risparmiata:", totalJoulesConsumption - postJoules)
        print("Risparmio massimo:", f"{(totalEmissionsConsumption - postEmissions + myInfrastructure[maxNode]["profile"]["carbon"]) / totalEmissionsConsumption * 100:.3f}%", 
            "\ngCO2/h risparmiata:", totalEmissionsConsumption - postEmissions + myInfrastructure[maxNode]["profile"]["carbon"], 
            "\nJoules/h risparmiata:", totalJoulesConsumption - postJoules + myInfrastructure[maxNode]["profile"]["carbon"])

    # Find the max consumption for all our estimates
    maxIstio = max(finalIstio, key=lambda x: x['emissions'])
    maxKepler = max(finalKepler, key=lambda x: x['emissions'])
    #maxVolume = max(finalVolume, key=lambda x: x['volume'])
    maxAll = max(maxIstio['emissions'], maxKepler['emissions'])
    maxNode = max(myInfrastructure, key=lambda x: myInfrastructure[x]["profile"]["carbon"])

    # Filer only the consumption above the threshold, which are to our interest
    monitorIstio = checkThreshold(finalIstio, 'emissions', maxIstio['emissions'], commThreshold)
    monitorKepler = checkThreshold(finalKepler, 'emissions', maxKepler['emissions'], serviceThreshold)
    #monitorVolume = checkThreshold(finalVolume, 'volume', maxVolume['volume'], volumeThreshold)
                
    monitorIstio = sorted(monitorIstio, key=lambda x: x['emissions'], reverse=True)
    #monitorVolume = sorted(monitorVolume, key=lambda x: x['volume'], reverse=True)
    prologFacts = []
    constraints = []
    constraintsHistory = []
    singleInstanceConstraints = []

    totalJoulesConsumption = 0
    totalEmissionsConsumption = 0
    totalJoulesSaved = 0
    totalEmissionsSaved = 0

    # Prolog file preparation

    # For each communication in our Istio metrics, save the fact
    for comm in finalIstio:
        fact = f"serviceConnection({comm["source"]}, {comm["destination"]}, {comm["emissions"]}, {comm["joules"]})"
        prologFacts.append(fact)
        totalEmissionsConsumption += comm['emissions']
        totalJoulesConsumption += comm['joules']
    # For each service in our Kepler metrics, save the fact    
    for service in finalKepler:
        fact = f"service({service["service"]}, {service["emissions"]}, {service["joules"]})"
        prologFacts.append(fact)
        totalEmissionsConsumption += service['emissions']
        totalJoulesConsumption += service['joules']
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
        #rule = f"highConsumptionConnection({comm['source']},{findFlavour(comm['source'], deploymentinfo)},{comm['destination']},{findFlavour(comm['destination'], deploymentinfo)},{float(comm['emissions'] / maxAll):.3f})"
        constraint = f"affinity({comm['source']},{findFlavour(comm['source'], deploymentinfo)},{comm['destination']},{findFlavour(comm['destination'], deploymentinfo)},{float(comm['emissions'] / maxAll):.3f})"
        constraintData = {
            "category": "affinity",
            "source": comm["source"],
            "source_flavour": findFlavour(comm['source'], deploymentinfo),
            "destination": comm["destination"],
            "destination_flavour": findFlavour(comm['destination'], deploymentinfo),
            "constraint_emissions": comm['emissions']
        }
        constraintsHistory.append(constraintData)
        #prologFacts.append(rule)
        constraints.append(constraint)
        totalEmissionsSaved += float(comm['emissions'])
        totalJoulesSaved += float(comm['joules'])

    # For each service of interest, save that there is an avoid
    for service in monitorKepler:
        serviceWeight = float(service['emissions'] / maxAll)
        for node in myInfrastructure:
            nodeWeight = float(myInfrastructure[node]["profile"]["carbon"] / myInfrastructure[maxNode]["profile"]["carbon"])
            scaledWeight = nodeWeight * serviceWeight
            #rule = f"highConsumptionService({service["service"]},{findFlavour(service['service'], deploymentinfo)}, {node}, {scaledWeight:.3f})"
            constraint = f"avoid({service["service"]},{findFlavour(service['service'], deploymentinfo)},{node},{scaledWeight:.3f})"
            if(scaledWeight > serviceThreshold):
                singleInst = {
                    "category": "avoid",
                    "source": service["service"],
                    "flavour": findFlavour(service['service'], deploymentinfo),
                    "node": node,
                    "constraint_emissions": service["emissions"]
                }
                singleInstanceConstraints.append(singleInst)
                #prologFacts.append(rule)
                constraints.append(constraint)
    
    #produceSavingsOut()

    return constraintsHistory, singleInstanceConstraints, maxAll, prologFacts