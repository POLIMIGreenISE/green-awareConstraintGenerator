import yaml
from collections import defaultdict

class InfrastructureHandler:
    def __init__(self, infrastructure_file):
        self.infrastructure_file = infrastructure_file
        self.infrastructure_info = None

    def handle_infrastructure(self):
        """Loads the infrastructure information from the file."""
        with open(self.infrastructure_file, "r") as file:
            self.infrastructure_info = yaml.safe_load(file)
        return self.infrastructure_info