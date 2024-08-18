import os

os.system("mkdir virtual_dropbox")
os.system("mkdir virtual_dropbox/interventions")
os.system("mkdir virtual_dropbox/observations")
os.system("python launch_experiment.py")
print("=======================================")
experiment = 0
for iteration in range(0,2):
    os.system(f"python virtual_medea.py 0 {iteration}")
    print("=======================================")
    os.system(f"python virtual_mombot.py 0 {iteration}")
    print("=======================================")

