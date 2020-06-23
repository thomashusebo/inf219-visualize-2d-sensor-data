import os
import time
import pandas as pd

'''Change these parameters to alter the instrument simulator'''
print_progress=True
wait_between_measurements=False
measurements_per_second = 2
project_name = "ObsFlow0Days.csv"

# Setting directories
projectName = project_name
file = os.getcwd() + "\\projects\\" + projectName
dir_temp = '../incoming_data'
if print_progress:
    print("\nReading data from " + file)
    print("Project data will be stored in: " + dir_temp)

# Getting the project file
df = pd.read_csv(file)

# Produce individual measurements
for i in range(df.shape[0]):
    out_df = pd.DataFrame(data=df.iloc[[i]])
    filename=dir_temp+"\\data{:09d}.csv".format(i)
    out_df.to_csv(filename, index=False)
    if print_progress:
        print("Created file {}".format(filename))
    if wait_between_measurements:
        time.sleep(1/measurements_per_second)
if print_progress:
    print("All files read, ending...")
