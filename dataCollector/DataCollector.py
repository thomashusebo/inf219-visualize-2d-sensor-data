import json
import os
from os import listdir
from os.path import isfile, join

available = True
myPath = "C:\\Users\\huseb\\PycharmProjects\\inf219-visualize-2d-sensor-data\\ignoreDir\\measurements"


def getData(data):
    files = [f for f in listdir(myPath) if isfile(join(myPath, f))]

    for file in files:
        with open('ignoreDir/measurements/'+file, 'r') as json_file:
            data.append(json.load(json_file))
            with open('ignoreDir/completedMeasurements/' + file + '.txt', 'w') as outfile:
                json.dump(data, outfile)
            outfile.close()
        os.remove(myPath + "\\" +file)
    return data