from pyswip import Prolog

# Create the prolog file and execute it
def createPrologFile(filename, facts):
    with open(filename, 'w') as file:
        for fact in facts:
            file.write(fact + ".\n")

    Prolog().consult("rules.pl")    