import multiprocessing
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

name = ''


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


class LoadProjectWindow(Screen):
    @staticmethod
    def select_project(project):
        global name
        name = project
        App.get_running_app().stop()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("setupapp\\setup.kv")


class SetupApp(App):
    def build(self):
        return kv
