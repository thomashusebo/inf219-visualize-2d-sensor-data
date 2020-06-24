import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

name = ''
#projects = next(os.walk(os.getcwd() + '\\projects'))[1]


class MainWindow(Screen):
    pass


class NewProjectWindow(Screen):
    project_name = ObjectProperty(None)

    def start_new_project(self):
        global name
        name = self.project_name.text
        App.get_running_app().stop()


class LoadProjectWindow(Screen):
    def select_project(self, project):
        global name
        name = project
        App.get_running_app().stop()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("setupapp\\setup.kv")


class SetupApp(App):

    def build(self):
        print("Building app")
        return kv
