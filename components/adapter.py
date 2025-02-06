from pyswip import Prolog

def createPrologFile(filename, facts):
    with open(filename, 'w') as file:
        for fact in facts:
            file.write(fact + ".\n")

    Prolog().consult("rules.pl")    