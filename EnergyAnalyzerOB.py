import os
from components.IstioHandler import IstioHandler
from components.keplerHandler import KeplerHandler
from components.deploymentHandler import DeploymentHandler
from components.infrastructureHandler import InfrastructureHandler
from components.consumptionEstimator import ConsumptionEstimator
from components.constraintsGenerator import ConstraintsGenerator
from components.knowledgeBaseHandler import KnowledgeBaseHandler
from components.weightGenerator import WeightGenerator
from components.adapter import Adapter
from components.Yamlmodifier import YamlModifier

# Define Input Files
rules = os.path.abspath("./rules.pl")
istio = os.path.abspath(os.path.join("input_files", "interaction3.csv"))
kepler = os.path.abspath(os.path.join("input_files", "service3.csv"))
deployment = os.path.abspath(os.path.join("input_files", "case_study_deployment.txt"))
infrastructure = os.path.abspath(os.path.join("input_files", "case_study_infra.yaml"))
knowledgeBase = os.path.abspath(os.path.join("output_files", "knowledgeBase.json"))
explanation = os.path.abspath(os.path.join("output_files", "explanation.txt"))
prologFactsFile = os.path.abspath("facts.pl")
prologConstraintFile = os.path.abspath("energyConstraints.pl")
yamlOutput = os.path.abspath(os.path.join("output_files", "EnergyEnhancer3.yaml"))
application = os.path.abspath(os.path.join("input_files", "app_case_study.yaml"))
changelog = os.path.abspath(os.path.join("output_files", "changelog.txt"))

infrastructureInformation = InfrastructureHandler(infrastructure).handle_infrastructure()
deploymentInformation = DeploymentHandler(deployment).handle_deployment()
newKepler = KeplerHandler(kepler).handler_kepler()
newIstio = IstioHandler(istio).handle_istio()
istioConsumptions, keplerConsumptions = ConsumptionEstimator(newIstio, newKepler, deploymentInformation).estimate_consumption()
affinityConstraints, avoidConstraints, highestConsumption, prologFacts = ConstraintsGenerator(istioConsumptions, keplerConsumptions, deploymentInformation, infrastructureInformation, knowledgeBase).generate_constraints()
finalConstraints = KnowledgeBaseHandler(knowledgeBase, istioConsumptions, keplerConsumptions, affinityConstraints, avoidConstraints, infrastructureInformation).handle_knowledgeBase()
finalPrologFacts = WeightGenerator(finalConstraints, prologFacts, deploymentInformation).generate_weights()
Adapter(rules, prologFactsFile, finalPrologFacts, prologConstraintFile, finalConstraints, explanation, yamlOutput).adapt_output()
YamlModifier(infrastructure, application, istioConsumptions, keplerConsumptions, changelog).modify_YAML()