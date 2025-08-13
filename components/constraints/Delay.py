class Delay:
    def __init__(self):
        self.delayConstraints = []

    def generate_constraints(self, deployment, myapp):
        # Given a service find which flavour it was deployed as
        def findFlavour(service, services):
            for s in services:
                if s["service"] == service:
                    return s["flavour"]

        for service in myapp["requirements"]["components"]:
            keywords = myapp["requirements"]["components"][service].get("common", {})
            if "delay" in keywords:
                delay = {
                    "category": "delay",
                    "source": service,
                    "flavour": findFlavour(service, deployment),
                    "delay": keywords["delay"]
                }
                self.delayConstraints.append(delay)

        return self.delayConstraints