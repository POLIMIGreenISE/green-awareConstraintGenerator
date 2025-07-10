import subprocess

node_values = range(100, 1001, 100)
service_values = range(100, 1001, 100)

for n in node_values:
    for s in service_values:
        print(f"Running: python3 EnergyAnalyzer.py -n {n} -s {s}")
        subprocess.run(["python3", "EnergyAnalyzer.py", "-n", str(n), "-s", str(s)])