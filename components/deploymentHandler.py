import json

# Handle the deployment informatio
def handleDeployment(deploymentFile):
    with open(deploymentFile, 'r') as file:
        deploymentinfo = json.load(file)
    return deploymentinfo