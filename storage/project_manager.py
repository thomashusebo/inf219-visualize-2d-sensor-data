import datetime
from bcrypt import checkpw
from pandas import read_sql_query
from sqlalchemy import create_engine, MetaData, Column, Table, String, inspect, Integer


class ProjectManager():
    def __init__(self):
        self.__master_database = "/storage/databases/master.db"
        db_engine = create_engine('sqlite://' + self.__master_database)
        self.__create_project_overview(db_engine)

    @staticmethod
    def __create_project_overview(db_engine):
        if not db_engine.dialect.has_table(db_engine, "projects"):
            meta = MetaData()
            Table(
                'projects', meta,
                Column('projectname', String, primary_key=True),
                Column('password', String),
                Column('created', String),
                Column('height', Integer),
                Column('width', Integer),
                Column('lastupdate', String)
            )
            meta.create_all(db_engine)

    def get_projects(self):
        db_engine = create_engine('sqlite://' + self.__master_database)
        query = "SELECT \"projectname\" FROM projects"
        return read_sql_query(query, db_engine)['projectname'].values

    def try_to_add_new_project_name(self, project_name, password, height, width):
        db_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "projectname" FROM projects WHERE "projectname"="{}"'.format(project_name)
        if read_sql_query(query, db_engine).empty:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S" )
            db_engine.execute(
                'INSERT INTO "projects" ("projectname", "password", "created", "height", "width") '
                'VALUES ("{}", "{}", "{}", "{}", "{}")'.format(project_name, password, timestamp, height, width))
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

    def get_dimensions(self, project_name):
        master_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "height", "width" FROM "projects" WHERE projectname = "{}"'.format(project_name)
        result = read_sql_query(query, master_engine)
        height = result['height'][0]
        width = result['width'][0]
        return height, width

    def get_last_timestamp(self, project_name):
        master_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "lastupdate" FROM "projects" WHERE projectname = "{}"'.format(project_name)
        result = read_sql_query(query, master_engine)
        return result['lastupdate'][0]

    def update_timestamp(self, project_name, last_timestamp):
        master_engine = create_engine('sqlite://' + self.__master_database)
        update = 'UPDATE "projects" SET "lastupdate" = "{}" WHERE "projectname" = "{}"'.format(
            last_timestamp,
            project_name)
        master_engine.execute(update)