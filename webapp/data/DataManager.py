from webapp.data.DataCollector import DataCollector
from sqlalchemy import create_engine

import os


class DataManager:
    def __init__(self, project_name):
        self.project_name = project_name
        database = create_engine('sqlite:///fluid_flower_database.db')
        chunksize = 10000
        self.data_collector = DataCollector(database, chunksize)

    def update(self):
        self.data_collector.update(self.data_collector)

    def get_data(self):
        return []

    def get_project_name(self):
        return self.project_name
