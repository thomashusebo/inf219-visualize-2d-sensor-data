from bcrypt import checkpw, hashpw
from pandas import read_sql_query

from sqlalchemy import create_engine, MetaData, Column, Table, String


class DatabaseManager():
    def __init__(self):
        self.__master_database = "/storage/databases/master.db"
        db_engine = create_engine('sqlite://' + self.__master_database)
        if not db_engine.dialect.has_table(db_engine, "projects"):
            meta = MetaData()
            Table(
                'projects', meta,
                Column('projectname', String, primary_key=True),
                Column('password', String)
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
            db_engine.execute('INSERT INTO "projects" ("projectname", "password") VALUES ("{}", "{}")'
                              .format(project_name, password))
            return True
        else:
            return False

    def verfiy_password(self, project_name, password):
        db_engine = create_engine('sqlite://' + self.__master_database)
        query = 'SELECT "password" FROM projects WHERE projectname = "{}"'.format(project_name)
        actual_encrypted_password = read_sql_query(query, db_engine)['password'][0][2:-1].encode()
        return checkpw(password.encode('utf-8'), actual_encrypted_password)
