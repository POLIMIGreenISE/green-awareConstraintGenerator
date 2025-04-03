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

        # Energy consumption for transferring 1 GB in KWh/GB
        energy_intensity = 0.0028125
        # Coefficient to convert 1 GB in kWh
        wattcoefficient = 0.0065

        # Given a service find which flavour it was deployed as
        def findFlavour(service, services):
            for s in services:
                if s["service"] == service:
                    return s["flavour"]
                
        self.finalIstio = []
        self.finalKepler = []

        for element in self.istio:
            # requestVolume measures the amount of requests in a span of 1 hour, multiplied by the average size of said requests
            data_transfer = (float(element["requestVolume"]) * float(element["requestSize"]) ) # / (1024 ** 3))
            # data_transfer (GB/h) * energy_intensity (kWh/GB) = kWh
            estimated_emissions = data_transfer /1000 #* wattcoefficient
            # Convert kWh to Joules
            joules = (estimated_emissions) * 1000
            consumption = {"source": element["source"], "source_flavour": findFlavour(element["source"], self.deployment), 
                        "destination": element["destination"], "destination_flavour": findFlavour(element["destination"], self.deployment),
                        "emissions": estimated_emissions, "joules": joules}
            self.finalIstio.append(consumption)

        for key, total in self.kepler.items():
            estimated_emissions = (total / 24) / 1000
            joules = {"service": key, "flavour": "large", "emissions": estimated_emissions, "joules": total /12}
            self.finalKepler.append(joules)
        return self.finalIstio, self.finalKepler    