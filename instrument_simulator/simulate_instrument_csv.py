import os
import time
import pandas as pd

if __name__ == "__main__":

    '''Change these parameters to alter the instrument simulator'''
    print_progress=True
    wait_between_measurements=True
    measurements_per_second = 1
    project_name = "ObsFlow1Days.csv"

    # Setting directories
    projectName = project_name
    file = os.getcwd() + "\\instrument_simulator\\projects\\" + projectName
    dir_temp = 'incoming_data'
    if print_progress:
        print("\nReading data from " + file)
        print("Project data will be stored in: " + dir_temp)

    # Getting the project file
    df = pd.read_csv(file)

    # Produce individual measurements
    for i in range(df.shape[0]):
        out_df = pd.DataFrame(data=df.iloc[[i]])
        filename=dir_temp+"/data{:09d}.csv".format(i)
        out_df.to_csv(filename, index=False)
        if print_progress:
            print("Created file {}".format(filename))
        if wait_between_measurements:
            time.sleep(1/measurements_per_second)
    if print_progress:
        print("All files read, ending...")
