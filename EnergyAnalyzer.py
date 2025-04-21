import os
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

# Define Input Files
rules = os.path.abspath("./rules.pl")
istio = os.path.abspath(os.path.join("input_files", "istio_data_default.json"))
kepler = os.path.abspath(os.path.join("input_files", "kepler-metrics.txt"))
nodes = os.path.abspath(os.path.join("input_files", "infra_OB_US.yaml"))
deployment = os.path.abspath(os.path.join("input_files", "deployment_US.txt"))
infrastructure = os.path.abspath(os.path.join("input_files", "infra_OB_US.yaml"))
knowledgeBase = os.path.abspath(os.path.join("output_files", "knowledgeBase.json"))
explanation = os.path.abspath(os.path.join("output_files", "explanation.txt"))
prologFactsFile = os.path.abspath("facts.pl")
prologConstraintFile = os.path.abspath("energyConstraints.pl")
yamlOutput = os.path.abspath(os.path.join("output_files", "EnergyEnhancer.yaml"))
application = os.path.abspath(os.path.join("input_files", "app_OB.yaml"))
changelog = os.path.abspath(os.path.join("output_files", "changelog.txt"))

infrastructureInformation = InfrastructureHandler(infrastructure).handle_infrastructure()
deploymentInformation = DeploymentHandler(deployment).handle_deployment()
newKepler = KeplerHandler(kepler).handler_kepler()
newIstio = IstioHandler(istio).handle_istio()
energyMix = EnergyMixGatherer(nodes)
istioConsumptions, keplerConsumptions = ConsumptionEstimator(newIstio, newKepler, deploymentInformation).estimate_consumption()
affinityConstraints, avoidConstraints, highestConsumption, prologFacts = ConstraintsGenerator(istioConsumptions, keplerConsumptions, deploymentInformation, infrastructureInformation, knowledgeBase, energyMix).generate_constraints()
finalConstraints = KnowledgeBaseHandler(knowledgeBase, istioConsumptions, keplerConsumptions, affinityConstraints, avoidConstraints, infrastructureInformation, energyMix).handle_knowledgeBase()
finalPrologFacts = WeightGenerator(finalConstraints, prologFacts, deploymentInformation).generate_weights()
Adapter(rules, prologFactsFile, finalPrologFacts, prologConstraintFile, finalConstraints, explanation, yamlOutput).adapt_output()
YamlModifier(infrastructure, application, istioConsumptions, keplerConsumptions, changelog, energyMix).modify_YAML()