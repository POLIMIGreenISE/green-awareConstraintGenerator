from datetime import datetime

# Gather the energy mix based on the current hour of the day
def gatherEnergyMix(energyMix, node):
    current_hour = datetime.now().hour
    current_mix = None
    for entry in energyMix[node]:
        entry_hour = datetime.fromisoformat(entry["timestamp"]).hour
        if entry_hour == current_hour:
            current_mix = entry["mix"]
            break
    return current_mix