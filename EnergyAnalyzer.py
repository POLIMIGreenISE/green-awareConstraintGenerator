import argparse, os, time, yaml, random
from components.IstioHandler import IstioHandler
from components.KeplerHandler import KeplerHandler
from components.DeploymentHandler import DeploymentHandler
from components.InfrastructureHandler import InfrastructureHandler
from components.ConsumptionEstimator import ConsumptionEstimator
from components.ConstraintsGenerator import ConstraintsGenerator
from components.KnowledgeBaseHandler import KnowledgeBaseHandler
from components.WeightGenerator import WeightGenerator
from components.Adapter import Adapter
from components.Yamlmodifier import YamlModifier
from components.EnergyMixGatherer import EnergyMixGatherer
from codecarbon import OfflineEmissionsTracker

num_components = 1000
num_nodes = 1000
minenergy = 100
maxenergy = 900
app1kpath = os.path.abspath(os.path.join("input_files", "app1k.yaml"))
nodes1kpath = os.path.abspath(os.path.join("input_files", "nodes1k.yaml"))

app1k = {
    "name": "onlineboutique",
    "components": {},
    "requirements": {
        "components": {},
        "dependencies": [],
        "budget": {
            "cost": 2000000,
            "carbon": 2000000
        }
    }
}
for i in range(num_components):
    comp_name = f"comp{i}"
    energy_value = random.randint(minenergy, maxenergy)

    app1k["components"][comp_name] = {
        "flavours": {
            "tiny": {
                "uses": [],
                "energy": energy_value
            }
        },
        "importance_order": ["tiny"]
    }
    app1k["requirements"]["components"][comp_name] = {
        "common": {
            "subnet": ["private"],
            "security": ["ssl"]
        },
        "flavour-specific": {
            "tiny": {
                "cpu": 1,
                "ram": 4,
                "availability": 99
            }
        }
    }
nodes1k = {
    "name": "onlineboutique",
    "nodes": {},
    "links": {}
}
for i in range(num_nodes):
    node_name = f"node{i}"
    carbon_value = random.randint(minenergy, maxenergy)

    nodes1k["nodes"][node_name] = {
        "capabilities": {
            "cpu": 8,
            "ram": 16,
            "storage": 1024,
            "availability": 99,
            "subnet": ["private"],
            "security": ["ssl", "firewall"]
        },
        "profile": {
            "cost": 10,
            "carbon": carbon_value
        }
    }
    nodes1k["links"] = {
        "connected_nodes": [],
        "capabilities": {
            "latency": 10,
            "availability": 99
        }
    }
with open(app1kpath, "w") as f:
    yaml.dump(app1k, f)
with open(nodes1kpath, "w") as f:
    yaml.dump(nodes1k, f)

tracker = OfflineEmissionsTracker(country_iso_code="ITA")
tracker.start()
start = time.perf_counter()

# Define Input Files
rules = os.path.abspath("./rules.pl")
istio = os.path.abspath(os.path.join("input_files", "istio_data_default.json"))
kepler = os.path.abspath(os.path.join("input_files", "kepler-metrics.txt"))
knowledgeBase = os.path.abspath(os.path.join("output_files", "knowledgeBase.json"))
explanation = os.path.abspath(os.path.join("output_files", "explanation.txt"))
prologFactsFile = os.path.abspath("facts.pl")
prologConstraintFile = os.path.abspath("energyConstraints.pl")
yamlOutput = os.path.abspath(os.path.join("output_files", "EnergyEnhancer.yaml"))
application = os.path.abspath(os.path.join("input_files", "app_OB.yaml"))
changelog = os.path.abspath(os.path.join("output_files", "changelog.txt"))

parser = argparse.ArgumentParser(description="FREEDA Energy Analyzer")
parser.add_argument('--region', '-r', 
                    choices=['eu', 'us'], 
                    required=False, 
                    help="The region that should be utilised for the infrastructure")
parser.add_argument('--keep', '-k', action='store_true',
                    help="Keep the current knowledge base, should not be kept if switching between regions",
                    required=False)
parser.add_argument('--scenario', '-s',
                    choices=['node', 'service', 'comm'],
                    required=False,
                    help="Define which scenario to run. Node modifies the energy mix of the nodes." \
                    "Service modifies the energy consumption of the services." \
                    "Comm modifies the communication intensity between services, simulating more users.")
args = parser.parse_args()
if args.region == "eu":
    nodes = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
    deployment = os.path.abspath(os.path.join("input_files", "deployment_EU.txt"))
    infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
elif args.region == "us":
    nodes = os.path.abspath(os.path.join("input_files", "infra_OB_US.yaml"))
    deployment = os.path.abspath(os.path.join("input_files", "deployment_US.txt"))
    infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_US.yaml"))
else:
    nodes = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
    deployment = os.path.abspath(os.path.join("input_files", "deployment_EU.txt"))
    infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))

if not args.keep:
    open(knowledgeBase, "w").close()

infrastructureInformation = InfrastructureHandler(infrastructure).handle_infrastructure()
deploymentInformation = DeploymentHandler(deployment).handle_deployment()
newKepler = KeplerHandler(kepler).handler_kepler()
newIstio = IstioHandler(istio).handle_istio()
energyMix = EnergyMixGatherer(nodes)

istioConsumptions, keplerConsumptions = ConsumptionEstimator(newIstio, newKepler, deploymentInformation).estimate_consumption()
affinityConstraints, avoidConstraints, highestConsumption, prologFacts = ConstraintsGenerator(istioConsumptions, keplerConsumptions, deploymentInformation, infrastructureInformation, knowledgeBase, energyMix).generate_constraints()
finalConstraints = KnowledgeBaseHandler(knowledgeBase, istioConsumptions, keplerConsumptions, affinityConstraints, avoidConstraints, infrastructureInformation, energyMix).handle_knowledgeBase()
finalPrologFacts = WeightGenerator(finalConstraints, prologFacts, deploymentInformation).generate_weights()
Adapter(rules, prologFactsFile, finalPrologFacts, prologConstraintFile, finalConstraints, explanation, yamlOutput, infrastructureInformation, energyMix).adapt_output()
YamlModifier(infrastructure, application, istioConsumptions, keplerConsumptions, changelog, energyMix).modify_YAML()

time.sleep(10)
end = time.perf_counter()
tracker.stop()
print(f"Execution time: {end - start:.7f} seconds")