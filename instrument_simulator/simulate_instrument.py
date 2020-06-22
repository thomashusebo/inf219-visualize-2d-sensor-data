import datetime
import json
import os
import time
from os import listdir
from os.path import isfile, join
from random import random

dir_existing_projects = '../../projects'
dir_temp = ""
files = []
simulationStart = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
speedUp = 60

print("Setup project...")

while True:
    print("\nEnter a unique project ID:")
    projectName = input()

    dir_original_data = dir_existing_projects + '\\'+ projectName + '\\induvidual_measurements'
    dir_temp = '../../projects/temp/' + projectName

    try:
        files = [f for f in listdir(dir_original_data) if isfile(join(dir_original_data, f))]
        print("Found %d data files:" % len(files))
    except FileNotFoundError:
        print("--ERROR: Did not find data in existing project")
        continue

    try:
        # Create target Directory
        os.mkdir(dir_temp)
        print("Directory ", dir_temp, " created ")
        break
    except FileExistsError:
        print("--ERROR: ", dir_temp, " already exists")
        print("--Do you wish to overwrite (y/n):")
        if input() == 'y':
            break


print("\nReading data from " + dir_original_data)
print("Project data will be stored in: " + dir_temp)

print("Press ENTER when ready")
input()

firstFile = True
projectStartTime = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")

for file in files:
    print("\nAttempting to read file: " + file)
    with open(dir_original_data + "\\" + file, 'r') as json_file:
        print("reading file: " + file)
        data = json.load(json_file)

        # Find when project started, only for first file
        #if firstFile:
        #    firstTimeStamp = data['ts'][0][0]
        #    projectStartTime = datetime.datetime.strptime(firstTimeStamp, "%H:%M:%S")
        #    firstFile = False

        # When was the file completed/how much time have elapsed in the project
        #lastTimeStamp = data['ts'][0][0]
        #then = datetime.datetime.strptime(lastTimeStamp, "%H:%M:%S")
        #timeIntoProject = then - projectStartTime

        # Simulate the original time series
        #
        #while True:
        #    now = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        #    timeSinceSimulationStart = (now - simulationStart)*speedUp
        #    print("Project time elapsed (speedup x" + str(speedUp) + "): " + str(timeSinceSimulationStart))
        #    if timeSinceSimulationStart > timeIntoProject:
        #        break
        #    time.sleep(1)
        time.sleep(1)

        with open(dir_temp + "/" + file, 'w') as outfile:
            json.dump(data, outfile)
        outfile.close()
    json_file.close()

print("All files read, ending...")
