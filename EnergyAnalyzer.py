import argparse, os, time, yaml, random, json
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

def generate_rnd(value):
    num_components = value
    num_nodes = value
    deployment1k = []
    kepler1k = []
    istio1k = []
    minenergy = 100
    maxenergy = 1800
    app1kpath = os.path.abspath(os.path.join("input_files", f"app{value}.yaml"))
    nodes1kpath = os.path.abspath(os.path.join("input_files", f"nodes{value}.yaml"))
    deployment1kpath = os.path.abspath(os.path.join("input_files", f"deployment{value}.txt"))
    kepler1kpath = os.path.abspath(os.path.join("input_files", f"kepler-metrics{value}.txt"))
    istio1kpath = os.path.abspath(os.path.join("input_files", f"istio_data_default{value}.json"))

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
        deploy1k_string = f"Component comp{i} deployed in flavour large on node node{i%num_nodes}."
        deployment1k.append(deploy1k_string)
        kepler1k_string = f"kepler_container_platform_joules_total{{container_id=\"{i}\",container_name=\"server\",container_namespace=\"default\",mode=\"dynamic\",pod_name=\"{comp_name}-minikube\",source=\"trained_power_model\"}} {energy_value}"
        kepler1k.append(kepler1k_string)
        istio_field = {
            "source": comp_name,
            "destination": f"comp{(i+1)%num_components}",
            "requestVolume": random.randint(int(minenergy / 10), int(maxenergy / 10)),
            "requestDuration": random.randint(1, 4),
            "requestSize": 1,
            "requestThroughput": random.randint(minenergy, maxenergy),
            "responseSize": random.randint(minenergy, maxenergy),
            "responseThroughput": random.randint(minenergy, maxenergy)
        }
        istio1k.append(istio_field)

        app1k["components"][comp_name] = {
            "flavours": {
                "large": {
                    "uses": [],
                    "energy": energy_value
                }
            },
            "importance_order": ["large"]
        }
        app1k["requirements"]["components"][comp_name] = {
            "common": {
                "subnet": ["private"],
                "security": ["ssl"]
            },
            "flavour-specific": {
                "large": {
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
        carbon_value = random.randint(minenergy, int(maxenergy / 2))

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
    with open(deployment1kpath, "w") as f:
        for line in deployment1k:
            f.write(str(line) + "\n")
        f.write("Objective value: 13" + "\n")
        f.write("\t" + "Total cost: 85" + "\n")
        f.write("\t" + "Total carb: 4194" + "\n")
    with open(kepler1kpath, "w") as f:
        for line in kepler1k:
            f.write(str(line) + "\n")    
    with open(istio1kpath, "w") as f:
        json.dump(istio1k, f, indent=4)

    return [
        app1kpath,
        nodes1kpath,
        deployment1kpath,
        kepler1kpath,
        istio1kpath
    ]

tracker = OfflineEmissionsTracker(country_iso_code="ITA")
tracker.start()
start = time.perf_counter()

# Define Input Files
rules = os.path.abspath("./rules.pl")
knowledgeBase = os.path.abspath(os.path.join("output_files", "knowledgeBase.json"))
explanation = os.path.abspath(os.path.join("output_files", "explanation.txt"))
prologFactsFile = os.path.abspath("facts.pl")
prologConstraintFile = os.path.abspath("energyConstraints.pl")
yamlOutput = os.path.abspath(os.path.join("output_files", "EnergyEnhancer.yaml"))
changelog = os.path.abspath(os.path.join("output_files", "changelog.txt"))

parser = argparse.ArgumentParser(description="FREEDA Energy Analyzer")
parser.add_argument('--region', '-r', 
                    choices=['eu', 'us', '100', '1k'], 
                    required=False, 
                    help="The region that should be utilised for the infrastructure")
parser.add_argument('--keep', '-k', action='store_true',
                    help="Keep the current knowledge base, should not be kept if switching between regions",
                    required=False)
args = parser.parse_args()
if args.region == "eu":
    istio = os.path.abspath(os.path.join("input_files", "istio_data_default.json"))
    kepler = os.path.abspath(os.path.join("input_files", "kepler-metrics.txt")) 
    nodes = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
    deployment = os.path.abspath(os.path.join("input_files", "deployment_EU.txt"))
    infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
    application = os.path.abspath(os.path.join("input_files", "app_OB.yaml"))
elif args.region == "us":
    istio = os.path.abspath(os.path.join("input_files", "istio_data_default.json"))
    kepler = os.path.abspath(os.path.join("input_files", "kepler-metrics.txt"))    
    nodes = os.path.abspath(os.path.join("input_files", "infra_OB_US.yaml"))
    deployment = os.path.abspath(os.path.join("input_files", "deployment_US.txt"))
    infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_US.yaml"))
    application = os.path.abspath(os.path.join("input_files", "app_OB.yaml"))
elif args.region == "100":
    a,n,d,k,i = generate_rnd(100)
    istio = i
    kepler = k
    nodes = n
    deployment = d
    infrastructure = n
    application = a
elif args.region == "1k":
    a,n,d,k,i = generate_rnd(1000)
    istio = i
    kepler = k
    nodes = n
    deployment = d
    infrastructure = n
    application = a
else:
    istio = os.path.abspath(os.path.join("input_files", "istio_data_default.json"))
    kepler = os.path.abspath(os.path.join("input_files", "kepler-metrics.txt"))
    nodes = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
    deployment = os.path.abspath(os.path.join("input_files", "deployment_EU.txt"))
    infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_EU.yaml"))
    application = os.path.abspath(os.path.join("input_files", "app_OB.yaml"))

if not args.keep:
    open(knowledgeBase, "w").close()

infrastructureInformation = InfrastructureHandler(infrastructure).handle_infrastructure()
deploymentInformation = DeploymentHandler(deployment).handle_deployment()
newKepler = KeplerHandler(kepler).handler_kepler()
newIstio = IstioHandler(istio).handle_istio()
energyMix = EnergyMixGatherer(nodes)

print("Estimating Consumptions...")
istioConsumptions, keplerConsumptions = ConsumptionEstimator(newIstio, newKepler, deploymentInformation).estimate_consumption()
print("Generating Constraints...")
affinityConstraints, avoidConstraints, highestConsumption, prologFacts = ConstraintsGenerator(istioConsumptions, keplerConsumptions, deploymentInformation, infrastructureInformation, application, knowledgeBase, energyMix).generate_constraints()
print("Consulting KnowledgeBase...")
finalConstraints = KnowledgeBaseHandler(knowledgeBase, istioConsumptions, keplerConsumptions, affinityConstraints, avoidConstraints, infrastructureInformation, energyMix).handle_knowledgeBase()
print("Generating Weights...")
finalPrologFacts = WeightGenerator(finalConstraints, prologFacts, deploymentInformation).generate_weights()
print("Adapting the outputs...")
Adapter(rules, prologFactsFile, finalPrologFacts, prologConstraintFile, finalConstraints, explanation, yamlOutput, infrastructureInformation, energyMix).adapt_output()
print("Modifying YAML...")
YamlModifier(infrastructure, application, istioConsumptions, keplerConsumptions, changelog, energyMix).modify_YAML()

end = time.perf_counter()
tracker.stop()
print(f"Execution time: {end - start:.7f} seconds")