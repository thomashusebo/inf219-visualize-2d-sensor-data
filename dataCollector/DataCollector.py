import json
import os
from os import listdir
from os.path import isfile, join

from factory import FigureCreator

available = True
myPath = "C:\\Users\\huseb\\PycharmProjects\\inf219-visualize-2d-sensor-data\\ignoreDir\\tempDirMeasurements"


def getData(data, projectName):
    path = myPath + "\\" + projectName
    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:
        #print("\nAttempt reading file " + file)
        try:
            with open('ignoreDir/tempDirMeasurements/' + projectName + "/" + file, 'r') as json_file:
                data.append(json.load(json_file))
                n = len(data)
                with open('ignoreDir/completedMeasurements/' + projectName + file + '.txt', 'w') as outfile:
                    json.dump(data[n-1], outfile)
            outfile.close()
            os.remove(path + "\\" + file)
            #print("...Reading Complete")
        except (FileNotFoundError, PermissionError):
            # Then file should've been read by another process
            # TODO: Assuming this can only happen when processes interfere with each other,
            # TODO: Add a way to monitor this as it is a symptom of another problem: conflicting processes.
            #print("...Reading failed")
            continue

    return data
