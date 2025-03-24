import json
import math
from datetime import datetime

# Energy consumption for transferring 1 GB in KWh/GB
energy_intensity = 0.0028125
# Coefficient to convert 1 GB in kWh
wattcoefficient = 0.0065

# From the service metric files obtain the consumption values for each service and each connection
def estimateConsumptions(istio, kepler, energyMix, deploymentInfo):

    # Simulate more traffic during busy hours
    def traffic_multiplier(hour):
        if 6 <= hour <= 24:  
            peak_hour = 16
            sigma = 7
            multiplier = math.exp(-((hour - peak_hour) ** 2) / (2 * sigma ** 2))
            return multiplier
        else:
            return 0.35

    def simulate_traffic(base_value):
        current_hour = datetime.now().hour
        multiplier = traffic_multiplier(current_hour)
        return base_value * multiplier

    def truncate_string(s):
        reversed_s = s[::-1]
        parts = reversed_s.split('-', 2)
        return parts[-1][::-1]
    
    # Given a service find which flavour it was deployed as
    def findFlavour(service, services):
        for s in services:
            if s["service"] == service:
                return s["flavour"]

    finalIstio = []
    finalKepler = []
    
    # Open the istio file. We already handled kepler outside and have the json ready.
    with open(istio, 'r') as file:
        metrics = json.load(file)
    keplerMetrics = json.loads(kepler)

    for element in metrics:
        # requestVolume measures the amount of requests in a span of 1 hour, multiplied by the average size of said requests
        data_transfer = (float(element["requestVolume"]) * float(element["requestSize"]) / (1024 ** 3))
        # data_transfer (GB/h) * energy_intensity (kWh/GB) = kWh
        #estimated_emissions = (1.5 + 0.03*data_transfer)
        estimated_emissions = data_transfer * wattcoefficient
        # Convert kWh to Joules
        joules = (estimated_emissions) * 1000
        consumption = {"source": element["source"], "source_flavour": findFlavour(element["source"], deploymentInfo), 
                       "destination": element["destination"], "destination_flavour": findFlavour(element["destination"], deploymentInfo),
                       "emissions": estimated_emissions, "joules": joules}
        finalIstio.append(consumption)

    # Define the important fields to take from the Kepler
    importantKeplerMetrics = ["kepler_container_platform_joules_total"]
    for metric in keplerMetrics:
        if metric["field"] in importantKeplerMetrics:
            metric["values"] = sorted(metric["values"], key=lambda x: float(x["value"]), reverse=True)[:]
            for pod in metric["values"]:
                if pod["container_name"] == "server":
                    # Jh / 1000 = KWh
                    estimated_emissions = simulate_traffic(float(pod["value"])) / 1000
                    joules = {"service": truncate_string(pod["pod_name"]), "flavour": findFlavour(truncate_string(pod["pod_name"]), deploymentInfo), 
                              "emissions": estimated_emissions, "joules": simulate_traffic(float(pod["value"]))}
                    finalKepler.append(joules)
    print(finalIstio)
    return finalIstio, finalKepler