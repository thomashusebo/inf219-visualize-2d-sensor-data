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

    # Data for data collector report
    debug = True
    num_read_files = 0
    num_deleted_files = 0
    num_files_not_found = 0
    num_files_with_permission_errors = 0
    num_files_with_empty_data_errors = 0
    if debug:
        all_read_files = []
        all_deleted_files = []
        all_files_not_found = []
        all_files_with_permission_errors = []
        all_files_with_empty_data_errors = []

    while True:
        files = next(os.walk(incoming_data_dir))[2]
        for file in files:
            if time_to_stop(stopping_dir, stopping_file):
                return "DataCollector Stopped. \n" \
                       "\t# files read: {} \n" \
                       "\t# files deleted: {} \n" \
                       "\t# files not found: {} \n" \
                       "\t# files with permission error: {} \n" \
                       "\t# files with EmptyDataError: {}".format(num_read_files,
                                                                num_deleted_files,
                                                                num_files_not_found,
                                                                num_files_with_permission_errors,
                                                                num_files_with_empty_data_errors,)
            try:
                file_dir = "{}\\{}".format(incoming_data_dir, file)
                for df in pd.read_csv(file_dir, chunksize=chunksize, iterator=True):
                    df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
                    df.to_sql(database_table, database, if_exists='append')

                num_read_files += 1
                if debug:
                    all_read_files.append(file_dir)

                os.remove(file_dir)

                num_deleted_files += 1
                if debug:
                    all_deleted_files.append(file_dir)

            except FileNotFoundError:
                # If file not found then another process completed and deleted it for the dir
                num_files_not_found += 1
                if debug:
                    all_files_not_found.append(file_dir)
                pass
            except PermissionError:
                # Then directly interfering with another process
                num_files_with_permission_errors += 1
                if debug:
                    all_files_with_permission_errors.append(file_dir)
                pass
            except pd.errors.EmptyDataError:
                # Trying to read incomplete file. Pass for now, will read fine when instrument have completed the file
                num_files_with_empty_data_errors += 1
                if debug:
                    all_files_with_empty_data_errors.append(file_dir)
                pass

            except Exception as e:
                if debug:
                    return "Unexpected error: {}. \n" \
                           "Trying to read file {}. \n\n" \
                           "All files read({}): {} \n\n" \
                           "All files deleted({}): {} \n\n" \
                           "All files not found({}): {} \n\n" \
                           "All files with permission error({}): {} \n\n" \
                           "All files with EmptyDataError ({})".format(e, file_dir,
                                                                       len(all_read_files), all_read_files,
                                                                       len(all_deleted_files), all_deleted_files,
                                                                       len(all_files_not_found),
                                                                       all_files_not_found,
                                                                       len(all_files_with_permission_errors),
                                                                       all_files_with_permission_errors)
                else:
                    return "Unexpected error: {}. \n" \
                           "Trying to read file {}. \n" \
                           "# files read: {} \n" \
                           "# files deleted: {} \n" \
                           "# files not found: {} \n" \
                           "# files with permission error: {} \n" \
                           "# files with EmptyDataError: {}".format(e, file_dir,
                                                                    num_read_files,
                                                                    num_deleted_files,
                                                                    num_files_not_found,
                                                                    num_files_with_permission_errors,
                                                                    num_files_with_empty_data_errors,)
