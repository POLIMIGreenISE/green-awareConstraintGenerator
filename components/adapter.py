from pyswip import Prolog

# Create the prolog file and execute it
def adaptOutput(filename, facts, generalConstraints, singleConstraints, explanationfile):
    def explain(constrType):
        match constrType:
            case "affinity":
                return "since the services exchanged a lot of data between them"
            case "avoid":
                return "since the services used a lot of resources and the node has a poor energy mix"

    with open(filename, 'w') as file:
        for fact in facts:
            file.write(fact + ".\n")

    Prolog().consult("rules.pl")

    with open(explanationfile, "w") as explfile:
        for constraint in generalConstraints:
            explanation = (f"A constrant of {constraint["category"]} was generated " 
                f"between {constraint["source"]} in flavour {constraint["source_flavour"]} "
                f"and {constraint["destination"]} in flavour {constraint["destination_flavour"]} "
                f"{explain(constraint["category"])}\n")
            explfile.write(explanation)
            
        for constraint in singleConstraints:
            explanation = (f"A constrant of {constraint["category"]} was generated " 
                f"between {constraint["source"]} in flavour {constraint["flavour"]} "
                f"and {constraint["node"]} {explain(constraint["category"])}\n"
                )

            explfile.write(explanation)