import os
from components import *

# Define Input Files
istio = os.path.abspath(os.path.join("files", "istio_data_default.json"))
kepler = os.path.abspath(os.path.join("files", "kepler-metrics.txt"))
deployment = os.path.abspath(os.path.join("files", "deployment_example.json"))
infrastructure = os.path.abspath(os.path.join("files", "infrastructure_example.yaml"))
knowledgeBase = os.path.abspath(os.path.join("files", "knowledgeBase.json"))
energyMix = os.path.abspath(os.path.join("files", "energyMix_timeSeries.json"))

myInfrastructure = prepareInfrastructure(infrastructure)
deploymentInfo = prepareDeploymentInfo(deployment)
ist, kep, vol = prepareValues(istio, prepareKepler(kepler), energyMix, deploymentInfo)
constr, singleInstanceConstr, maxConsumption, prologFacts = prepareConstraints(ist, kep, vol, deploymentInfo, myInfrastructure)
final_constraints = handleKnowledgeBase(knowledgeBase, ist, kep, constr)
final_prologFacts = weightGenerator(final_constraints, singleInstanceConstr, maxConsumption, prologFacts)
createPrologFile("facts.pl", final_prologFacts)