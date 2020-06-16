from webapp.data import DataCollector


class DataManager:
    def __init__(self, project_name):
        self.data = []
        self.project_name = project_name

    def update(self):
        DataCollector.getData(self.data, self.project_name)

    def get_data(self):
        return self.data

    def get_project_name(self):
        return self.project_name
