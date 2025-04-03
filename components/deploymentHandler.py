import json
import re

class DeploymentHandler:
    def __init__(self, deployment_file):
        self.deployment_file = deployment_file
        self.deployment_info = None

    def handle_deployment(self):
        """Loads the deployment information from the file."""
        with open(self.deployment_file, "r") as file:
            text = file.read()

        pattern = r"Component (\w+) deployed in flavour (\w+) on node (\w+)."

        self.deploymentinfo = [
            {"service": match.group(1), "flavour": match.group(2), "node": match.group(3)}
            for match in re.finditer(pattern, text)
        ]

        return self.deploymentinfo