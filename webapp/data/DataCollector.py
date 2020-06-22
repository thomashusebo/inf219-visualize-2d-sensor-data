import os
import pandas as pd


class DataCollector:
    def __init__(self, database, chunksize):
        self.incoming_data_dir = os.getcwd() + '\\incoming_data'
        print(self.incoming_data_dir)
        self.database = database
        self.chunksize = chunksize

    @staticmethod
    def update(self):
        files = next(os.walk(self.incoming_data_dir))[2]
        database_table = 'resistivity'

        for file in files:
            file_dir = "{}\\{}".format(self.incoming_data_dir,file)
            for df in pd.read_csv(file_dir, chunksize=self.chunksize, iterator=True):
                df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
                df.to_sql(database_table, self.database, if_exists='append')

            os.remove(file_dir)

    @staticmethod
    def get_data():
        return []
