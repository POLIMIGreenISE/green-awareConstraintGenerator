import statistics
from collections import defaultdict
import csv
import os
import yaml

class EnergyMixGatherer:
    def __init__(self, node):
        self.node = node
        self.mix = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "input_files", "node2.csv"))
        #os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "input_files", "case_study_infra.yaml"))

    def gather_energyMix(self):
        """Gather the energy mix based on the node."""
        
        sums = defaultdict(lambda: {"sum": 0.0, "count": 0.0})
        with open(self.mix, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["callback_id"] == "featured_carbon":
                    key = row["node_id"]
                    sums[key]["sum"] += float(row["value"])
                    sums[key]["count"] += 1
        

        # with open(self.mix, "r") as file:
        #     myInfra = yaml.safe_load(file)
        # myEnergyMix = {
        #     node: [{"mix": details["profile"]["carbon"]}]
        #     for node, details in myInfra["nodes"].items()
        # }
        
        return int(sums[self.node]["sum"] / sums[self.node]["count"]) #statistics.mean(x["mix"] for x in myEnergyMix[self.node])