import os
import time
import pandas as pd
from sqlalchemy import create_engine
from data.data_types import DataType


def time_to_stop(stopping_dir):
    files = next(os.walk(stopping_dir))[2]
    for file in files:
        if file == 'stop.txt':
            os.remove(stopping_dir + '\\stop.txt')
            return True
    return False


def update(project_name):
    incoming_data_dir = os.getcwd() + '\\incoming_data'
    stopping_dir = os.getcwd() + '\\data\\stopping_data_collector'
    database = create_engine('sqlite:///fluid_flower_database.db')
    chunksize = 100000
    project_name = project_name
    resistivity_table = "{}_{}".format(project_name, DataType.Resistivity.value)
    database_table = resistivity_table

    while True:
        if time_to_stop(stopping_dir):
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

    return "DataCollector completed"


def tell_to_stop():
    f = open("data/stopping_data_collector/stop.txt", 'w')
    f.close()
