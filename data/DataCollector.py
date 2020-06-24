import os
import pandas as pd
from sqlalchemy import create_engine
from data.datatypes import DataType


class DataCollector:
    def __init__(self, project_name):
        self.incoming_data_dir = os.getcwd() + '\\incoming_data'
        self.database = create_engine('sqlite:///fluid_flower_database.db')
        self.chunksize = 100000
        self.project_name = project_name
        self.resistivity_table = "{}_{}".format(project_name, DataType.Resistivity.value)

    @staticmethod
    def update(self):
        while True:
            files = next(os.walk(self.incoming_data_dir))[2]
            database_table = self.resistivity_table

            for file in files:
                try:
                    file_dir = "{}\\{}".format(self.incoming_data_dir, file)
                    for df in pd.read_csv(file_dir, chunksize=self.chunksize, iterator=True):
                        df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
                        df.to_sql(database_table, self.database, if_exists='append')

                    os.remove(file_dir)
                except FileNotFoundError:
                    print("{} not found".format(file))
                    #If file not found then another process completed and deleted it
                    pass
                except PermissionError:
                    print("{} not accesible".format(file))
                    # Then directly interfering with another process
                    continue