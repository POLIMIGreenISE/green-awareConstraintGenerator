import json
import math
import re
import yaml
from collections import defaultdict
from datetime import datetime
from pyswip import Prolog

# Define Input Files
istio = "istio_data_default.json"
kepler = "kepler-metrics.txt"
deployment = "deployment_example.json"
infrastructure = "infrastructure_example.yaml"
knowledgeBase = "knowledgeBase.json"
energyMix = "energyMix_timeSeries.json"

# Define constant values

# Energy consumption for transferring 1 GB in KWh/GB
energy_intensity = 0.0028125

# Threshold for service communications
commThreshold = 0.5
volumeThreshold = 0.5

# Threshold for services joule consumption
serviceThreshold = 0.8

# When constrainst should stop being produced
knowledgeBaseMemoryThreshold = 0.5

# From the kepler .txt obtain a JSON structure
def prepareKepler(keplerFile):
    data = defaultdict(dict)
    final = []

    with open(keplerFile, 'r') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#'):
                parts = re.split(r'[{}]', line)
                field = parts[0]
                data = parts[1]
                value = parts[2].strip()
                data = data.split(',')
                tojson = {}
                tojson["field"] = field
                for ele in data:
                    if '=' in ele:
                        key, value2 = ele.split('=', 1)
                        tojson[key] = value2.strip('"')
                tojson["value"] = value
                final.append(tojson)

    # Filter only the fields of a specific namespace
    def filterByNS(namespace):
        filter = [item for item in final if item.get("container_namespace") == namespace]
        grouped_data = defaultdict(list)
        for item in filter:
            field = item['field']
            grouped_data[field].append({
                "container_name": item['container_name'],
                "pod_name": item['pod_name'],
                "value": item['value']
            })
        final_data = []
        for field, values in grouped_data.items():
            final_data.append({
                "field": field,
                "values": values
            })
        return json.dumps(final_data, indent=4)

    # Request only the default namespace as that is where our microservices reside
    namespaces = ["default"]
    for ns in namespaces:
        return filterByNS(ns)
    
# Parse the infrastructure file
def prepareInfrastructure(yamlFile):
    with open(yamlFile, "r") as file:
        data = yaml.safe_load(file)

    def parseNestedDict(data, parent_key=""):
        fields = []
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                # Recursively parse nested dictionaries
                fields.extend(parseNestedDict(value, full_key))
            else:
                # Append key and value as a tuple
                fields.append((full_key, value))
        return fields

    fields = parseNestedDict(data['nodes'])

    # Initialize a nested defaultdict
    nested_dict = lambda: defaultdict(nested_dict)
    data = nested_dict()

    # Populate the nested dictionary
    for field_name, field_value in fields:
        keys = field_name.split('.')  # Split the field name into hierarchical levels
        d = data
        for key in keys[:-1]:  # Traverse and create intermediate levels
            d = d[key]
        d[keys[-1]] = field_value  # Set the final key's value

    # Convert back to a regular dict (optional)
    data = dict(data)
    return data

def prepareDeploymentInfo(deploymentFile):
    with open(deploymentFile, 'r') as file:
            deploymentinfo = json.load(file)

    return deploymentinfo

# From the service metric files obtain the consumption values for each service and each connection
def prepareValues(istio, kepler):

    def traffic_multiplier(hour):
        if 8 <= hour <= 18:  
            peak_hour = 15
            sigma = 2    
            multiplier = math.exp(-((hour - peak_hour) ** 2) / (2 * sigma ** 2))
            return 0.5 + multiplier
        else:
            return 0.35

    def simulate_traffic(base_value):
        current_hour = datetime.now().hour
        multiplier = traffic_multiplier(current_hour)
        return base_value * multiplier

    def findNode(service, services):
        for s in services:
            if s["service"] == service:
                return s["node"]

    def truncate_string(s):
        reversed_s = s[::-1]
        parts = reversed_s.split('-', 2)
        return parts[-1][::-1]
    
    finalIstio = []
    finalKepler = []
    finalVolume = []
    
    with open(istio, 'r') as file:
        metrics = json.load(file)
    keplerMetrics = json.loads(kepler)

    with open(energyMix, 'r') as file:
        energymix = json.load(file)

    for element in metrics:
        # /1000 -> from ms to s
        # /2 from RTT to one way trip 
        # *200000 speed of light in fiber optics
        distance = (float(element["requestDuration"]) / 2000) * 200000
        # requestVolume measures the amount of requests in a span of 1 hour
        data_transfer = (float(element["requestVolume"]) * float(element["requestSize"]) / (1024 ** 3))
        # Scale Data Transfer
        data_transfer = data_transfer * 65000
        grid_intensity = prepareGridIntensity(energymix, findNode(element["source"], prepareDeploymentInfo(deployment)))
        # distance (km) * data_transfer (GB/h) * grid_intensity (gCO2e/kWh) * energy_intensity (kWh/GB/km) = gCO2e/h
        estimated_emissions = data_transfer * grid_intensity * energy_intensity
        joules = (estimated_emissions / grid_intensity) * 1000
        consumption = {"source": element["source"], "destination": element["destination"], "emissions": estimated_emissions, "joules": joules}
        volume = {"source": element["source"], "destination": element["destination"], "volume": data_transfer}
        finalIstio.append(consumption)
        finalVolume.append(volume)

    # Define the important fields to take from the Kepler
    importantKeplerMetrics = ["kepler_container_platform_joules_total"]

    for metric in keplerMetrics:
        if metric["field"] in importantKeplerMetrics:
            metric["values"] = sorted(metric["values"], key=lambda x: float(x["value"]), reverse=True)[:]
            for pod in metric["values"]:
                if pod["container_name"] == "server":
                    grid_intensity = prepareGridIntensity(energymix, findNode(truncate_string(pod["pod_name"]), prepareDeploymentInfo(deployment)))
                    estimated_emissions = (simulate_traffic(float(pod["value"])) / 1000) * grid_intensity
                    joules = {"service": truncate_string(pod["pod_name"]), "emissions": estimated_emissions, "joules": simulate_traffic(float(pod["value"]))}
                    finalKepler.append(joules)

    return finalIstio, finalKepler, finalVolume

# From the metrics, sorted from highest consumption to lowest, obtain the constraints to produce in output
def prepareConstraints(finalIstio, finalKepler, finalVolume):
    def checkThreshold(array, field, max, threshold):
        output = []
        for var in array:
            if float(var[field] > (max * threshold)):
                output.append(var)
        return output
    
    def findFlavour(service, services):
        for s in services:
            if s["service"] == service:
                return s["flavour"]

    # Print the total Emissions and the saved Emissions
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

    maxIstio = max(finalIstio, key=lambda x: x['emissions'])
    maxKepler = max(finalKepler, key=lambda x: x['emissions'])
    maxVolume = max(finalVolume, key=lambda x: x['volume'])
    maxAll = max(maxIstio['emissions'], maxKepler['emissions'])
    maxNode = max(myInfrastructure, key=lambda x: myInfrastructure[x]["profile"]["carbon"])

    monitorIstio = checkThreshold(finalIstio, 'emissions', maxIstio['emissions'], commThreshold)
    monitorKepler = checkThreshold(finalKepler, 'emissions', maxKepler['emissions'], serviceThreshold)
    monitorVolume = checkThreshold(finalVolume, 'volume', maxVolume['volume'], volumeThreshold)
                
    monitorIstio = sorted(monitorIstio, key=lambda x: x['emissions'], reverse=True)
    monitorVolume = sorted(monitorVolume, key=lambda x: x['volume'], reverse=True)
    prologFacts = []
    constraints = []
    constraintsHistory = []

    totalJoulesConsumption = 0
    totalEmissionsConsumption = 0
    totalJoulesSaved = 0
    totalEmissionsSaved = 0

    for comm in finalIstio:
        fact = f"serviceConnection({comm["source"]}, {comm["destination"]}, {comm["emissions"]}, {comm["joules"]})"
        prologFacts.append(fact)
        totalEmissionsConsumption += comm['emissions']
        totalJoulesConsumption += comm['joules']
    for service in finalKepler:
        fact = f"service({service["service"]}, {service["emissions"]}, {service["joules"]})"
        prologFacts.append(fact)
        totalEmissionsConsumption += service['emissions']
        totalJoulesConsumption += service['joules']
    for node in myInfrastructure:
        fact = f"node({node}, {myInfrastructure[node]["profile"]["carbon"]})"
        prologFacts.append(fact)
    deploymentinfo = prepareDeploymentInfo(deployment)
    for element in deploymentinfo:
        rule = f"deployedTo({element["service"]},{element["flavour"]},{element["node"]})"
        prologFacts.append(rule)
    for comm in monitorIstio:
        rule = f"highConsumptionConnection({comm['source']},{findFlavour(comm['source'], deploymentinfo)},{comm['destination']},{findFlavour(comm['destination'], deploymentinfo)},{float(comm['emissions'] / maxAll)})"
        constraint = f"affinity({comm['source']},{findFlavour(comm['source'], deploymentinfo)},{comm['destination']},{findFlavour(comm['destination'], deploymentinfo)},{float(comm['emissions'] / maxAll):.3f})"
        constraintData = {
            "category": "affinity",
            "source": comm["source"],
            "source_flavour": findFlavour(comm['source'], deploymentinfo),
            "destination": comm["destination"],
            "destination_flavour": findFlavour(comm['destination'], deploymentinfo),
            "constraint_weight": float(comm['emissions'] / maxAll)
        }
        constraintsHistory.append(constraintData)
        prologFacts.append(rule)
        constraints.append(constraint)
        totalEmissionsSaved += float(comm['emissions'])
        totalJoulesSaved += float(comm['joules'])
    for service in monitorKepler:
        serviceWeight = float(service['emissions'] / maxAll)
        for node in myInfrastructure:
            nodeWeight = float(myInfrastructure[node]["profile"]["carbon"] / myInfrastructure[maxNode]["profile"]["carbon"])
            scaledWeight = nodeWeight * serviceWeight
            rule = f"highConsumptionService({service["service"]},{findFlavour(service['service'], deploymentinfo)}, {node}, {scaledWeight})"
            constraint = f"avoid({service["service"]},{findFlavour(service['service'], deploymentinfo)},{node},{scaledWeight:.3f})"
            if(scaledWeight > serviceThreshold):
                prologFacts.append(rule)
                constraints.append(constraint)
    
    produceSavingsOut()

    return constraintsHistory, prologFacts
        
def handleKnowledgeBase(knowledgeBase, istio, kepler, constraints, rules):
    with open(knowledgeBase, "r") as file:
        myKnowledgeBase = yaml.safe_load(file)
    
    def sigmoid_decay_step(weight):
        k = 2
        multiplier = 1 / (1 + math.exp(k * (1 - weight)))
        new_weight = weight * multiplier
        return new_weight

    def createPrologFile(filename, facts):
        with open(filename, 'w') as file:
            for fact in facts:
                file.write(fact + ".\n")

    if not myKnowledgeBase:
        # We have no previous knowledge, save the basis
        services = []
        connections = []
        constr = []
        for element in kepler:
            past = []
            pastData = {
                "emissions": element["emissions"],
                "joules": element["joules"]
            }
            past.append(pastData)
            historyData = {
                "service": element["service"],
                "history": past
            }
            services.append(historyData)
        for element in istio:
            past = []
            pastData = {
                "emissions": element["emissions"],
                "joules": element["joules"]
            }
            past.append(pastData)
            historyData = {
                "source": element["source"],
                "destination": element["destination"],
                "history": past
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
                    pastData = {
                        "emissions": element["emissions"],
                        "joules": element["joules"]
                    }
                    service["history"].append(pastData)
                    service_found = True
                    break
            if not service_found:
                newKnowledge = {
                    "service": element["service"],
                    "history": [
                        {
                            "emissions": element["emissions"],
                            "joules": element["joules"]
                        }
                    ]
                }
                myKnowledgeBase["services"].append(newKnowledge) 
        for element in istio:
            pairing_found = False
            for connection in myKnowledgeBase["connections"]:
                if connection["source"] == element["source"] and connection["destination"] == element["destination"]:
                    pastData = {
                        "emissions": element["emissions"],
                        "joules": element["joules"]
                    }
                    connection["history"].append(pastData)
                    pairing_found = True
                    break
            if not pairing_found:
                newKnowledge = {
                    "source": element["service"],
                    "destination": element["destination"],
                    "history": [
                        {
                            "emissions": element["emissions"],
                            "joules": element["joules"]
                        }
                    ]
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

    for element in myKnowledgeBase["constraints"]:
        if knowledgeBaseMemoryThreshold < element["weight"] < 1.0:
            new_rule = f"highConsumptionConnection({element['source']},{element["source_flavour"]},{element['destination']},{element["destination_flavour"]},{element["constraint_weight"]})"
            rules.append(new_rule)
    createPrologFile("facts.pl", rules)   

def prepareGridIntensity(energyMix, node):
    current_hour = datetime.now().hour
    current_mix = None
    for entry in energyMix[node]:
        entry_hour = datetime.fromisoformat(entry["timestamp"]).hour
        if entry_hour == current_hour:
            current_mix = entry["mix"]
            break
    return current_mix

myInfrastructure = prepareInfrastructure(infrastructure)
ist, kep, vol = prepareValues(istio, prepareKepler(kepler))
constr, rules = prepareConstraints(ist, kep, vol)
handleKnowledgeBase(knowledgeBase, ist, kep, constr, rules)

Prolog().consult("rules.pl")