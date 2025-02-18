import json
import math
from datetime import datetime
from .energyMixGatherer import gatherEnergyMix

# Energy consumption for transferring 1 GB in KWh/GB
energy_intensity = 0.0028125

# From the service metric files obtain the consumption values for each service and each connection
def estimateConsumptions(istio, kepler, energyMix, deploymentInfo):

    # Simulate more traffic during busy hours
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

    # Given a service find the node it is deployed to
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
    #finalVolume = []
    
    # Open the istio file. We already handled kepler outside and have the json ready.
    with open(istio, 'r') as file:
        metrics = json.load(file)
    keplerMetrics = json.loads(kepler)

    with open(energyMix, 'r') as file:
        energymix = json.load(file)

    for element in metrics:
        # requestVolume measures the amount of requests in a span of 1 hour
        data_transfer = (float(element["requestVolume"]) * float(element["requestSize"]) / (1024 ** 3))
        # Scale Data Transfer
        data_transfer = data_transfer * 65000
        grid_intensity = gatherEnergyMix(energymix, findNode(element["source"], deploymentInfo))
        # data_transfer (GB/h) * grid_intensity (gCO2e/kWh) * energy_intensity (kWh/GB/km) = gCO2e/h
        estimated_emissions = data_transfer * grid_intensity * energy_intensity
        joules = (estimated_emissions / grid_intensity) * 1000
        consumption = {"source": element["source"], "destination": element["destination"], "emissions": estimated_emissions, "joules": joules}
        #volume = {"source": element["source"], "destination": element["destination"], "volume": data_transfer}
        finalIstio.append(consumption)
        #finalVolume.append(volume)

    # Define the important fields to take from the Kepler
    importantKeplerMetrics = ["kepler_container_platform_joules_total"]

    for metric in keplerMetrics:
        if metric["field"] in importantKeplerMetrics:
            metric["values"] = sorted(metric["values"], key=lambda x: float(x["value"]), reverse=True)[:]
            for pod in metric["values"]:
                if pod["container_name"] == "server":
                    grid_intensity = gatherEnergyMix(energymix, findNode(truncate_string(pod["pod_name"]), deploymentInfo))
                    estimated_emissions = (simulate_traffic(float(pod["value"])) / 1000) * grid_intensity
                    joules = {"service": truncate_string(pod["pod_name"]), "emissions": estimated_emissions, "joules": simulate_traffic(float(pod["value"]))}
                    finalKepler.append(joules)

    return finalIstio, finalKepler