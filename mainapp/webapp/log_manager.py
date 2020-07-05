from pandas import read_sql_query, DataFrame
from sqlalchemy import create_engine, MetaData, Table, Column, BIGINT, String


class LogManager:
    def __init__(self, project_name):
        self.database = create_engine('sqlite:///storage/databases/{}.db'.format(project_name))
        self.project_name = project_name
        if not self.database.dialect.has_table(self.database, "log"):
            meta = MetaData()
            Table(
                'log', meta,
                Column('index', BIGINT),
                Column('timestamp', String),
                Column('entry', String)
            )
            meta.create_all(self.database)

    def insert_log_entry(self, timestamp, log_entry):
        new_entry = DataFrame({'timestamp': [timestamp], 'entry':[log_entry]})
        new_entry.to_sql("log", self.database, if_exists='append')

    def retrieve_log(self):
        log = ''''''
        query = 'SELECT * FROM "log"'
        log_entries = read_sql_query(query, self.database)
        for i in range(log_entries.shape[0]):
            entry = log_entries['entry'][i]
            if entry is None: entry = ""
            log += '\n --- \n **' + log_entries['timestamp'][i] + '** \n\n' + entry
        return log


