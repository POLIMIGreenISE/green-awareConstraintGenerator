import json

class IstioHandler:
    def __init__(self, istio_file):
        self.istio_file = istio_file
        self.metrics = None

    def handle_istio(self):
        """Loads the Istio metrics from the file."""
        with open(self.istio_file, 'r') as file:
            self.metrics = json.load(file)
        return self.metrics