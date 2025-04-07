import csv
import json
import re
from collections import defaultdict

class IstioHandler:
    def __init__(self, istio_file):
        self.istio_file = istio_file
        self.metrics = None

    def handle_istio(self):
        """Loads the Istio metrics from the file."""
        # with open(self.istio_file, 'r') as file:
        #     self.metrics = json.load(file)
        # Replace the flavour subfix that was introduced during Eclypse
        with open(self.istio_file, "r") as f:
            reader = csv.reader(f)
            rows = [[re.sub(r'_(large|medium|tiny)', '', cell) for cell in row] for row in reader]
        with open(self.istio_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        self.metrics = defaultdict(float)
        with open(self.istio_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["callback_id"] == "interaction_energy":
                    key = (row["source"], row["target"])
                    self.metrics[key] += float(row["value"])
        return self.metrics