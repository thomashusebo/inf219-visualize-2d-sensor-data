import datetime
from bcrypt import checkpw
from pandas import read_sql_query
from sqlalchemy import create_engine, MetaData, Column, Table, String, inspect


class ProjectManager():
    def __init__(self):
        self.__master_database = "/storage/databases/master.db"
        db_engine = create_engine('sqlite://' + self.__master_database)
        if not db_engine.dialect.has_table(db_engine, "projects"):
            meta = MetaData()
            Table(
                'projects', meta,
                Column('projectname', String, primary_key=True),
                Column('password', String),
                Column('created', String)
            )
            meta.create_all(db_engine)

    def get_projects(self):
        db_engine = create_engine('sqlite://' + self.__master_database)
        query = "SELECT \"projectname\" FROM projects"
        return read_sql_query(query, db_engine)['projectname'].values

    def try_to_add_new_project_name(self, project_name, password):
        db_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "projectname" FROM projects WHERE "projectname"="{}"'.format(project_name)
        if read_sql_query(query, db_engine).empty:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S" )
            db_engine.execute('INSERT INTO "projects" ("projectname", "password", "created") VALUES ("{}", "{}", "{}")'
                              .format(project_name, password, timestamp))
            return True
        else:
            return False

    def verify_password(self, project_name, password):
        db_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "password" FROM projects WHERE projectname = "{}"'.format(project_name)
        actual_encrypted_password = read_sql_query(query, db_engine)['password'][0][2:-1].encode()
        return checkpw(password.encode('utf-8'), actual_encrypted_password)

    def export_project(self, project_name):
        master_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "created" FROM "projects" WHERE projectname = "{}"'.format(project_name)
        timestamp = read_sql_query(query, master_engine)['created'][0]
        project_engine = create_engine(('sqlite:///storage/databases/' + project_name + ".db"))
        inspector = inspect(project_engine)
        for table in inspector.get_table_names():
            query = 'SELECT * FROM "{}"'.format(table)
            df = read_sql_query(query, project_engine)
            filename = 'export/{}_{}_{}.csv'.format(timestamp, project_name, table)
            df.to_csv(filename, index=False)
