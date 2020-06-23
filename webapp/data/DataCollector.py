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
            file_dir = "{}\\{}".format(self.incoming_data_dir, file)
            for df in pd.read_csv(file_dir, chunksize=self.chunksize, iterator=True):
                df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})

                print(df.head)
                df.to_sql(database_table, self.database, if_exists='append')

            os.remove(file_dir)

        # TODO: REMOVE AFTER TESTING
        #print("Heatmap data:")
        #print(self.get_heatmap_data(self=self, timestamp="18:31:08"))
        #print("Linechart data:")
        #print(self.get_linechart_data(self=self, cell_x=1, cell_y=1, start_time="18:30:00", end_time="21:00:00"))

    @staticmethod
    def get_heatmap_data(self, timestamp):
        height = 7  # TODO Get height and width from database
        width = 13
        columns = "".join(["\"[{:02d},{:02d}]\",".format(x, y) for y in range(height) for x in range(width)])[:-1]
        sql_query = 'SELECT {} FROM {} WHERE time = \"{}\"'.format(
                columns,
                self.resistivity_table,
                timestamp)
        heatmap_data = pd.read_sql_query(sql_query, self.database)
        return heatmap_data.values.reshape(height, width)

    @staticmethod
    def get_linechart_data(self, coordinate, timeline):
        time_column = "time"
        cell_column = "[{:02d},{:02d}]".format(coordinate['x'], coordinate['y'])
        linechart_data = pd.read_sql_query(
            'SELECT \"{}\",\"{}\" FROM {} WHERE "time" BETWEEN \"{}\" AND \"{}\"'.format(
                time_column, cell_column, self.resistivity_table, timeline['start'], timeline['end']),
            self.database)
        return linechart_data
