import os
from components import *

# Define Input Files
istio = os.path.abspath(os.path.join("files", "istio_data_default.json"))
kepler = os.path.abspath(os.path.join("files", "kepler-metrics.txt"))
deployment = os.path.abspath(os.path.join("files", "deployment_example.json"))
infrastructure = os.path.abspath(os.path.join("files", "infrastructure_example.yaml"))
knowledgeBase = os.path.abspath(os.path.join("files", "knowledgeBase.json"))
energyMix = os.path.abspath(os.path.join("files", "energyMix_timeSeries.json"))
explanation = os.path.abspath(os.path.join("files", "explanation.txt"))
plFacts = os.path.abspath("facts.pl")

infrastructureInformation = handleInfrastructure(infrastructure)
deploymentInformation = handleDeployment(deployment)
istioConsumptions, keplerConsumptions = estimateConsumptions(istio, handleKepler(kepler), energyMix, deploymentInformation)
energyConstraints, singleInstanceConstraints, highestConsumption, prologFacts = generateConstraints(istioConsumptions, keplerConsumptions, deploymentInformation, infrastructureInformation)
finalConstraints = handleKnowledgeBase(knowledgeBase, istioConsumptions, keplerConsumptions, energyConstraints)
finalPrologFacts = generateWeights(finalConstraints, singleInstanceConstraints, highestConsumption, prologFacts)
adaptOutput(plFacts, finalPrologFacts, finalConstraints, singleInstanceConstraints, explanation)