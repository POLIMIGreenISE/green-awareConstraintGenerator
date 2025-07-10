import subprocess

for i in range(1, 6):
    print(f"\n--- Run #{i} ---")
    subprocess.run(["python3", "run_all.py"])