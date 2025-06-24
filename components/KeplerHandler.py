import json
import re
from collections import defaultdict

class KeplerHandler:
    def __init__(self, kepler_file):
        self.kepler_file = kepler_file
        self.metrics = None

    def handler_kepler(self):
        """Loads the Kepler metrics from the file."""
        data = defaultdict(dict)
        final = []

        # Open the file
        with open(self.kepler_file, 'r') as file:
            # Read line by line
            for line in file:
                # Obtain the parts useful to us
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