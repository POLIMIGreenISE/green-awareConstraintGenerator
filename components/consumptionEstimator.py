import json
import math
from datetime import datetime

class ConsumptionEstimator:
    def __init__(self, istio, kepler, deployment):
        self.istio = istio
        self.kepler = kepler
        self.deployment = deployment
        self.istioConsumption = None
        self.keplerConsumption = None

    def estimate_consumption(self):
        """Estimates the kW/h consumption starting from the monitoring metrics for each service and each connection."""

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

        # Energy consumption for transferring 1 GB in KWh/GB
        energy_intensity = 0.0028125
        # Coefficient to convert 1 GB in kWh
        wattcoefficient = 0.0065

        # Given a service find which flavour it was deployed as
        def findFlavour(service, services):
            for s in services:
                if s["service"] == service:
                    return s["flavour"]
                
        self.istioConsumption = []
        self.keplerConsumption = []

        for element in self.istio:
            # requestVolume measures the amount of requests in a span of 1 hour, multiplied by the average size of said requests
            data_transfer = (float(element["requestVolume"]) * float(element["requestSize"]) / (1024 ** 3))
            # data_transfer (GB/h) * energy_intensity (kWh/GB) = kWh
            estimated_emissions = data_transfer /1000 * wattcoefficient
            # Convert kWh to Joules
            joules = (estimated_emissions) * 1000
            consumption = {"source": element["source"], "source_flavour": findFlavour(element["source"], self.deployment), 
                        "destination": element["destination"], "destination_flavour": findFlavour(element["destination"], self.deployment),
                        "emissions": estimated_emissions, "joules": joules}
            self.istioConsumption.append(consumption)

        # Define the important fields to take from the Kepler
        importantKeplerMetrics = ["kepler_container_platform_joules_total"]
        self.kepler = json.loads(self.kepler)
        for metric in self.kepler:
            if metric["field"] in importantKeplerMetrics:
                metric["values"] = sorted(metric["values"], key=lambda x: float(x["value"]), reverse=True)[:]
                for pod in metric["values"]:
                    if pod["container_name"] == "server":
                        # Jh / 1000 = KWh
                        estimated_emissions = simulate_traffic(float(pod["value"])) / 1000
                        joules = {"service": truncate_string(pod["pod_name"]), "flavour": findFlavour(truncate_string(pod["pod_name"]), self.deployment), 
                                "emissions": estimated_emissions, "joules": simulate_traffic(float(pod["value"]))}
                        self.keplerConsumption.append(joules)

        return self.istioConsumption, self.keplerConsumption