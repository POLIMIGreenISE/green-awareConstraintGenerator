average_global = 100
multiplier = 0.75

def generateWeights(constraints, singleInstanceConstr, maxConsumption, prologFacts):
    # Generate the weights of our constraints
    # Given an average global gco2e consumtpion
    # If our services consume below
    # Give them a malus multiplier
    for constr in constraints:
        if maxConsumption < average_global:
            final_weight = constr["constraint_emissions"] * multiplier
            final_weight = final_weight / average_global
        elif constr["constraint_emissions"] < average_global:
            final_weight = constr["constraint_emissions"] * multiplier
            final_weight = final_weight / maxConsumption
        else:
            final_weight = constr["constraint_emissions"] / maxConsumption
        new_rule = f"highConsumptionConnection({constr['source']},{constr["source_flavour"]},{constr['destination']},{constr["destination_flavour"]},{final_weight:.3f})"
        prologFacts.append(new_rule)

    for constr in singleInstanceConstr:
        if maxConsumption < average_global:
            final_weight = constr["constraint_emissions"] * multiplier
            final_weight = final_weight / average_global
        elif constr["constraint_emissions"] < average_global:
            final_weight = constr["constraint_emissions"] * multiplier
            final_weight = final_weight / maxConsumption
        else:
            final_weight = constr["constraint_emissions"] / maxConsumption
        new_rule = f"highConsumptionService({constr["source"]},{constr["flavour"]},{constr["node"]},{final_weight:.3f})"
        prologFacts.append(new_rule)

    return prologFacts