import argparse
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


def run(
    rules,
    interaction,
    service,
    nodes,
    deployment,
    application,
    infrastructure,
    kb,
    explanation,
    facts,
    prologConstraints,
    yamlConstraints,
    changelog
):
    infrastructureInformation = InfrastructureHandler(infrastructure).handle_infrastructure()
    deploymentInformation = DeploymentHandler(deployment).handle_deployment()
    newKepler = KeplerHandler(service).handler_kepler()
    newIstio = IstioHandler(interaction).handle_istio()
    energyMix = EnergyMixGatherer(nodes)
    istioConsumptions, keplerConsumptions = ConsumptionEstimator(newIstio, newKepler, deploymentInformation).estimate_consumption()
    affinityConstraints, avoidConstraints, _, prologFacts = ConstraintsGenerator(istioConsumptions, keplerConsumptions, deploymentInformation, infrastructureInformation, kb).generate_constraints()
    finalConstraints = KnowledgeBaseHandler(kb, istioConsumptions, keplerConsumptions, affinityConstraints, avoidConstraints, infrastructureInformation).handle_knowledgeBase()
    finalPrologFacts = WeightGenerator(finalConstraints, prologFacts, deploymentInformation).generate_weights()
    Adapter(rules, facts, finalPrologFacts, prologConstraints, finalConstraints, explanation, yamlConstraints).adapt_output()
    YamlModifier(infrastructure, application, istioConsumptions, keplerConsumptions, changelog).modify_YAML()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FREEDA main loop over ECLYPSE simulator")
    parser.add_argument("rules", type=str, help="Prolog rules ABSOLUTE file path")
    parser.add_argument("interaction", type=str, help="Interaction file path")
    parser.add_argument("service", type=str, help="Service file path")
    parser.add_argument("nodes", type=str, help="Nodes file path")
    parser.add_argument("deployment", type=str, help="Deployment file path")
    parser.add_argument("app", type=str, help="Application yaml file path")
    parser.add_argument("infrastructure", type=str, help="Infrastructure yaml file path")
    parser.add_argument("knowledge_base", type=str, help="Knowledge base file")
    parser.add_argument("explanation", type=str, help="Explanation output file path")
    parser.add_argument("facts", type=str, help="Prolog facts file path")
    parser.add_argument("prolog_constraints", type=str, help="Prolog constraint file path")
    parser.add_argument("constraints", type=str, help="Constraints output file path")
    parser.add_argument("changelog", type=str, help="Changelog output file path")
    args = parser.parse_args()

    run(
        args.rules,
        args.interaction,
        args.service,
        args.nodes,
        args.deployment,
        args.app,
        args.infrastructure,
        args.knowledge_base,
        args.explanation,
        args.facts,
        args.prolog_constraints,
        args.constraints,
        args.changelog
    )