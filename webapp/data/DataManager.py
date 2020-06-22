from webapp.data.DataCollector import DataCollector
from sqlalchemy import create_engine


@DeprecationWarning
class DataManager:
    def __init__(self, project_name):
        database = create_engine('sqlite:///fluid_flower_database.db')
        chunksize = 10000
        self.data_collector = DataCollector(database, chunksize, project_name)

    def update(self):
        self.data_collector.update(self.data_collector)

    def get_heatmap_data(self, timestamp):
        return self.data_collector.get_heatmap_data(timestamp)

    def get_linechart_data(self, cell_x, cell_y, start_time, end_time):
        return self.data_collector.get_linechart_data(cell_x, cell_y, start_time, end_time)

    def get_project_name(self):
        return self.data_collector.project_name
