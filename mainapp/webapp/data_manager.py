import time

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from mainapp.data.data_types import DataType


class DataManager:
    def __init__(self, project_name):
        self.database = create_engine('sqlite:///storage/databases/{}.db'.format(project_name))
        self.project_name = project_name
        self.resistivity_table = "{}_RAW".format(DataType.Resistivity.value)

    @staticmethod
    def get_heatmap_data(self, timestamp="", live=False):
        """
        :param self:
        :param timestamp: str
             representing time, must be formatted as YYYY-MM-DD HH:MM:SS
        :param live: bool
            whether or not to show latest data
        :return: numpy array
            Returns a numpy array of heatmap. If live, will return the latest data. If a timestamp is given, will
        return data for given heatmap if it exists.
        """

        # For now, there is only one table to choose from
        timing = {}
        first_tic = time.process_time()
        table = self.resistivity_table

        timing['live'] = live

        if timestamp is "" and not live:
            Exception("Illegal heatmap retrieval. No timestamp and not live")

        # Selects for which timestamp to show a heatmap
        tic = time.process_time()
        try:
            last_timestamp = pd.read_sql_query("SELECT MAX(\"time\") FROM {}".format(table),
                                               self.database).values[0][0]
        except sqlalchemy.exc.OperationalError:
            return None,[]

        if live:
            timestamp = last_timestamp
        toc = time.process_time()
        timing['find timestamp'] = toc-tic

        # Finds dimensions of the data
        tic = time.process_time()
        query = "SELECT /*+ MAX_EXECUTION_TIME(1000) */ \"width\",\"height\" FROM {} WHERE \"time\"=\"{}\"".format(table, timestamp)
        dimensions = pd.read_sql_query(query, self.database)
        if dimensions.empty:
            return None, []
        width = dimensions.values[0][0]
        height = dimensions.values[0][1]
        toc = time.process_time()
        timing['find dimensions'] = toc-tic


        # Collects a DataFrame of the heatmap
        tic = time.process_time()
        columns = "".join(["\"[{:02d},{:02d}]\",".format(x, y) for y in range(height) for x in range(width)])[:-1]
        sql_query = 'SELECT /*+ MAX_EXECUTION_TIME(1000) */ {} FROM {} WHERE time = \"{}\"'.format(
            columns,
            table,
            timestamp)
        heatmap_data = pd.read_sql_query(sql_query, self.database)
        toc = time.process_time()
        timing['collect data'] = toc-tic
        timing['complete time'] = toc-first_tic
        print("Collect map data: {}".format(timing))

        # Return a numpy array of the heatmap, reshaped to width and height of the data
        return last_timestamp, heatmap_data.values[0].reshape(height, width)

    @staticmethod
    def get_linechart_data(self, coordinates, timeline):
        """
        :param self:
        :param coordinate: dict
            {'x': x, 'y': y}. Used to select cell in heatmap
        :param timeline: dict
            {'start': "YYYY-MM-DD HH:MM:SS", 'end': "YYYY-MM-DD HH:MM:SS"}. Used to select range of x axis
        :return: pandas DataFrame

        """
        # For now, there is only one table to choose from
        table = self.resistivity_table

        columns = "\"time\""
        for coordinate in coordinates:
            columns += "".join(",\"[{:02d},{:02d}]\"".format(coordinate['x'],coordinate['y']))

        #columns = "".join(["\"[{:02d},{:02d}]\",".format(x, y) for y in range(height) for x in range(width)])[:-1]
        #columns = "\"time\",\"[{:02d},{:02d}]\"".format(coordinate['x'], coordinate['y'])

        try:
            linechart_data = pd.read_sql_query(
                'SELECT {} FROM {} WHERE "time" BETWEEN \"{}\" AND \"{}\"'.format(
                    columns, table, timeline['start'], timeline['end']),
                self.database)
        except sqlalchemy.exc.OperationalError:
            return pd.DataFrame()

        return linechart_data
