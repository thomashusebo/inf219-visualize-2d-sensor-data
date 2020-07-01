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

    database = create_engine('sqlite:///storage/databases/{}.db'.format(project_name))
    chunksize = 1000
    project_name = project_name
    resistivity_table = "{}_{}".format(project_name, DataType.Resistivity.value)
    database_table = resistivity_table

    # Data for data collector report
    collection_statistics = {
        "Files read: ": 0,
        "Chunks of last file read: ": 0,
        "Files deleted: ": 0,
        "Failed deletions: ": 0,
        "Files not found: ": 0,
        "Permission errors: ": 0,
        "Empty data errors: ": 0,
        "Failed initialization errors: ": 0
    }

    while True:
        files = next(os.walk(incoming_data_dir))[2]
        if time_to_stop(stopping_dir, stopping_file):
            return "DataCollector Stopped \n " + str(collection_statistics)
        for file in files:
            if time_to_stop(stopping_dir, stopping_file):
                return "DataCollector Stopped \n " + str(collection_statistics)

            try:
                tic = time.process_time()
                file_dir = "{}\\{}".format(incoming_data_dir, file)
                for df in pd.read_csv(file_dir, chunksize=chunksize, iterator=True):
                    if time_to_stop(stopping_dir, stopping_file):
                        return "DataCollector Stopped \n " + str(collection_statistics)
                    df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
                    df.to_sql(database_table, database, if_exists='append')
                    toc = time.process_time()
                    collection_statistics['Chunks of last file read: '] += chunksize
                    collection_statistics['Time until last chunk: '] = toc-tic
                toc = time.process_time()
                collection_statistics['Time to read last file: '] = toc-tic
                collection_statistics['Time until last chunk: '] = 0
                collection_statistics['Chunks of last file read: '] = 0
                collection_statistics['Files read: '] += 1
                os.remove(file_dir)
                toc = time.process_time()
                collection_statistics['Time to read and delete last file'] = toc-tic

                if file not in next(os.walk(incoming_data_dir))[2]:
                    collection_statistics['Files deleted: '] += 1
                else:
                    collection_statistics['Failed deletions: '] += 1

            except FileNotFoundError:
                # If file not found then another process completed and deleted it for the dir
                collection_statistics['Files not found: '] += 1
                pass

            except PermissionError:
                # Then directly interfering with another process
                collection_statistics['Permission errors: '] += 1
                pass

            except pd.errors.EmptyDataError:
                # Trying to read incomplete file. Pass for now, will read fine when instrument have completed the file
                collection_statistics['Empty data errors: '] += 1
                pass

            except OSError:
                # Trying to read a file that has not been completely transferred to dir
                collection_statistics['Failed initialization errors: '] += 1
                pass

            except Exception as e:
                return "Unexpected error: {}. \n" \
                        "Trying to read file {}. \n".format(e, file_dir) + str(collection_statistics)
