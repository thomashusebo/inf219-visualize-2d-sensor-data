import os
import time
import pandas as pd
from sqlalchemy import create_engine
from mainapp.data.data_types import DataType


def tell_to_stop():
    f = open("mainapp/termination/stop_dir/stop_data_collector.txt", 'w')
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


def update(project_name):
    incoming_data_dir = os.getcwd() + '\\incoming_data'

    stopping_dir = os.getcwd() + '\\mainapp\\termination\\stop_dir'
    stopping_file = 'stop_data_collector.txt'
    clean_up_stopping_dir(stopping_dir, stopping_file)

    database = create_engine('sqlite:///fluid_flower_database.db')
    chunksize = 100000
    project_name = project_name
    resistivity_table = "{}_{}".format(project_name, DataType.Resistivity.value)
    database_table = resistivity_table

    while True:
        if time_to_stop(stopping_dir, stopping_file):
            return "DataCollector Stopped"

        files = next(os.walk(incoming_data_dir))[2]
        for file in files:
            try:
                file_dir = "{}\\{}".format(incoming_data_dir, file)
                for df in pd.read_csv(file_dir, chunksize=chunksize, iterator=True):
                    df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
                    df.to_sql(database_table, database, if_exists='append')

                os.remove(file_dir)
            except FileNotFoundError:
                # If file not found then another process completed and deleted it
                pass
            except PermissionError:
                # Then directly interfering with another process
                pass
        time.sleep(1)
