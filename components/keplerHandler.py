import json
import re
from collections import defaultdict
import csv

class KeplerHandler:
    def __init__(self, kepler_file):
        self.kepler_file = kepler_file
        self.metrics = None

    def handler_kepler(self):
        """Loads the Kepler metrics from the file."""
        # Replace the flavour subfix that was introduced during Eclypse
        with open(self.kepler_file, "r") as f:
            reader = csv.reader(f)
            rows = [[re.sub(r'_(large|medium|tiny)', '', cell) for cell in row] for row in reader]
        with open(self.kepler_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        self.metrics = defaultdict(float)
        with open(self.kepler_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["callback_id"] == "service_energy":
                    key = row["service_id"]
                    self.metrics[key] += float(row["value"])
        return self.metrics