from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from sqlalchemy import create_engine, inspect

name = ''
inspector = inspect(create_engine('sqlite:///fluid_flower_database.db'))


class MainWindow(Screen):
    @staticmethod
    def quit():
        App.get_running_app().stop()


class NewProjectWindow(Screen):
    project_name = ObjectProperty(None)

    def start_new_project(self):
        global name
        name = self.project_name.text
        App.get_running_app().stop()


class ContinueProjectWindow(Screen):
    pass


class LoadProjectWindow(Screen):


    @staticmethod
    def select_project(project):
        global name
        name = project
        App.get_running_app().stop()

    @staticmethod
    def print_all_projects():
        print(inspector.get_table_names())
        print("Projects")


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("setupapp\\setup.kv")


class SetupApp(App):
    def build(self):
        return kv
