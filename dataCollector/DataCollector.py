import json
import os
from os import listdir
from os.path import isfile, join

available = True
myPath = "C:\\Users\\huseb\\PycharmProjects\\inf219-visualize-2d-sensor-data\\ignoreDir\\measurements"


def getData(data):
    files = [f for f in listdir(myPath) if isfile(join(myPath, f))]

    for file in files:
        print("\nAttempt reading file " + file)
        try:
            with open('ignoreDir/measurements/' + file, 'r') as json_file:
                data.append(json.load(json_file))
                with open('ignoreDir/completedMeasurements/' + file + '.txt', 'w') as outfile:
                    json.dump(data, outfile)
            outfile.close()
            os.remove(myPath + "\\" + file)
            print("...Reading Complete")
        except (FileNotFoundError, PermissionError):
            # Then file should've been read by another process
            # TODO: Assuming this can only happen when processes interfere with each other,
            # TODO: Add a way to monitor this as it is a symptom of another problem: conflicting processes.
            print("...Reading failed")
            continue

    return data
