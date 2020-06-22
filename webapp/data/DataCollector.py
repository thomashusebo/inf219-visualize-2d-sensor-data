import os
import pandas as pd
from sqlalchemy import create_engine
from webapp.data.datatypes import DataType


class DataCollector:
    def __init__(self, project_name):
        self.incoming_data_dir = os.getcwd() + '\\incoming_data'
        self.database = create_engine('sqlite:///fluid_flower_database.db')
        self.chunksize = 100000
        self.project_name = project_name
        self.resistivity_table = "{}_{}".format(project_name, DataType.Resistivity.value)

    @staticmethod
    def update(self):
        files = next(os.walk(self.incoming_data_dir))[2]
        database_table = self.resistivity_table

        for file in files:
            file_dir = "{}\\{}".format(self.incoming_data_dir,file)
            for df in pd.read_csv(file_dir, chunksize=self.chunksize, iterator=True):
                df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
                df.to_sql(database_table, self.database, if_exists='append')

            os.remove(file_dir)

    @staticmethod
    def get_heatmap_data(self, timestamp):
        heatmap_data = pd.read_sql_query(
            'SELECT * FROM {} WHERE time = {}'.format(
                self.resisitvity_table,
                timestamp),
            self.database)
        print(heatmap_data)
        return heatmap_data

    @staticmethod
    def get_linechart_data(self, cell_x, cell_y, start_time, end_time):
        time_column = ""
        cell_column = "[{:02d},{:02d}]".format(cell_x, cell_y)
        linechart_data = pd.read_sql_query(
            'SELECT {},{} FROM {} WHERE "time" BETWEEN {} AND {}'.format(
                time_column, cell_column, self.resistivity_table, start_time, end_time),
            self.database)
        print(linechart_data)
        return linechart_data
