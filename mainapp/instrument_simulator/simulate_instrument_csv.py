import os
import time
import pandas as pd


def tell_to_stop():
    f = open("mainapp/termination/stop_dir/stop_instrument_simulator.txt", 'w')
    f.close()


def time_to_stop(stopping_dir, stopping_file):
    files = next(os.walk(stopping_dir))[2]
    if stopping_file in files:
        os.remove(stopping_dir + '\\' + stopping_file)
        return True
    return False


def clean_up_stopping_dir(stopping_dir, stopping_file):
    files = next(os.walk(stopping_dir))[2]
    for file in files:
        if file == stopping_file:
            os.remove(stopping_dir + '\\' + stopping_file)


def run(measurements_per_second=None):
    stopping_dir = os.getcwd() + '\\mainapp\\termination\\stop_dir'
    stopping_file = 'stop_instrument_simulator.txt'
    clean_up_stopping_dir(stopping_dir, stopping_file)

    wait_between_measurements = True

    if measurements_per_second is None:
        wait_between_measurements = False

    relative_location = "\\mainapp\\instrument_simulator\\projects\\"
    dir = os.getcwd() + relative_location
    project_name = "ObsFlow0Days.csv"

    # Setting directories
    projectName = project_name
    file = dir + projectName
    dir_temp = 'incoming_data'

    # Getting the project file
    df = pd.read_csv(file)

    # Produce individual measurements
    for i in range(df.shape[0]):
        out_df = pd.DataFrame(data=df.iloc[[i]])
        filename = dir_temp + "/data{:09d}.csv".format(i)
        out_df.to_csv(filename, index=False)

        if time_to_stop(stopping_dir, stopping_file):
            return "Instrument simulation stopped"

        if wait_between_measurements:
            time.sleep(1 / measurements_per_second)

    return "Instrument simulation complete"
