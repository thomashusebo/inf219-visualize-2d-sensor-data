from sqlalchemy import create_engine

from mainapp.webapp.dataretriever import DataRetriever
from pandas import DataFrame, read_sql_query


def add_calibration(project_name, calibration_name, timestamp):
    engine = create_engine('sqlite:///storage/databases/{}.db'.format(project_name))
    calibration_data = DataFrame({'time': [timestamp], 'calibrationname': [calibration_name]})
    calibration_data.to_sql('calibration', engine, if_exists='append')


def get_map_calibration_data(project_name, timestamp):
    retriever = DataRetriever(project_name)
    _, map_data = retriever.get_heatmap_data(retriever, timestamp=timestamp)
    return map_data


def get_all_calibration_times(project_name):
    engine = create_engine('sqlite:///storage/databases/{}.db'.format(project_name))
    result = None
    if engine.dialect.has_table(engine, "calibration"):
        query = 'SELECT * FROM "calibration"'
        result = read_sql_query(query, engine)
    return result
