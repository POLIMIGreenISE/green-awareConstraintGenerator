import os
import yaml
from components.EnergyMixGatherer import EnergyMixGatherer

class YamlModifier:
    def __init__(self, infrastructure, application, istio, kepler, changelog):
        self.infrastructure = infrastructure
        self.application = application
        self.istio = istio
        self.kepler = kepler
        self.changelog= changelog
        self.changes = None

    def modify_YAML(self):
        """Generates the changes necessary for the output YAMLs."""
        def str_list_representer(dumper, data):
            return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
        yaml.add_representer(list, str_list_representer, Dumper=yaml.SafeDumper)

        with open(self.infrastructure, "r") as file:
            myInfrastructure = yaml.safe_load(file)
        with open(self.application, "r") as file:
            myApplication = yaml.safe_load(file)

        # infraOut = os.path.abspath(os.path.join("output_files", os.path.basename(self.infrastructure)))
        # appOut = os.path.abspath(os.path.join("output_files", os.path.basename(self.application)))
        self.changes = []

        for node in myInfrastructure["nodes"]:
            if myInfrastructure["nodes"][node]["profile"]["carbon"] != EnergyMixGatherer(node).gather_energyMix():
                nodestr = f"node {node} {EnergyMixGatherer(node).gather_energyMix()}"
                self.changes.append(nodestr)


        for service in myApplication["components"]:
            for flavour in myApplication["components"][service]["flavours"]:
                if [item for item in self.kepler if item["service"] == service and item["flavour"] == flavour]:
                    if myApplication["components"][service]["flavours"][flavour]["energy"] != int([item["emissions"] for item in self.kepler if item["service"] == service and item["flavour"] == flavour][0] * 1000):
                        servicestr = f"service {service} {flavour} {int([item["emissions"] for item in self.kepler if item["service"] == service and item["flavour"] == flavour][0] * 1000)}"
                        self.changes.append(servicestr)


        for service in myApplication["requirements"]["dependencies"]:
            for flavour in myApplication["requirements"]["dependencies"][service]:
                for connection in myApplication["requirements"]["dependencies"][service][flavour]:
                    if [item for item in self.istio if item["source"] == service and item["source_flavour"] == flavour and item["destination"] == connection]:
                        if myApplication["requirements"]["dependencies"][service][flavour][connection]["energy"] != int([item["emissions"] for item in self.istio if item["source"] == service and item["source_flavour"] == flavour and item["destination"] == connection][0] * 1000):
                            linkstr = f"link {service} {flavour} {connection} {int([item["emissions"] for item in self.istio if item["source"] == service and item["source_flavour"] == flavour and item["destination"] == connection][0] * 1000)}"
                            self.changes.append(linkstr)
        
        # with open(infraOut, "w") as file:
        #     yaml.dump(myInfrastructure, file, Dumper=yaml.SafeDumper)
        # with open(appOut, "w") as file:
        #     yaml.dump(myApplication, file, Dumper=yaml.SafeDumper)

        with open(self.changelog, "w") as f:
            for change in self.changes:
                f.write(change + "\n")