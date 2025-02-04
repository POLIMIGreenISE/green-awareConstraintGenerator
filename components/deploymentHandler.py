import json

def prepareDeploymentInfo(deploymentFile):
    with open(deploymentFile, 'r') as file:
        deploymentinfo = json.load(file)
    return deploymentinfo