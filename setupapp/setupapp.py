from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from storage.database_manager import DatabaseManager

active_project = ''
database_manager = DatabaseManager()
datacollection = False


class MainWindow(Screen):
    @staticmethod
    def quit():
        App.get_running_app().stop()


class NewProjectWindow(Screen):
    project_name = ObjectProperty(None)

    def start_new_project(self):
        name = self.project_name.text
        if database_manager.try_to_add_new_project_name(name):
            print("Succcesfully added {}".format(name))
        else:
            print("Unsuccesfull. {} already in database".format(name))


class ContinueProjectWindow(Screen):
    pass


class LoadProjectWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


def start_main_software(project, collect_data, instance):
    global active_project, datacollection
    print(project, collect_data)
    active_project = project
    datacollection = collect_data
    App.get_running_app().stop()


def return_to_main(instance):
    App.get_running_app().root.transition = SlideTransition(direction='right')
    App.get_running_app().root.current = 'main'


def get_go_back_button():
    go_back_button = Button(text="Go Back")
    go_back_button.bind(on_release=return_to_main)
    return go_back_button


class SetupApp(App):

    def build(self):
        kv = Builder.load_file("setupapp\\setup.kv")
        load_screen = kv.get_screen("load_project")
        continue_screen = kv.get_screen("continue_project")

        print(App.get_running_app().root.current)

        projects = database_manager.get_projects()
        for project in projects:
            load_button = Button(text=project)
            load_buttoncallback = partial(start_main_software, project, False)
            load_button.bind(on_release=load_buttoncallback)
            load_screen.children[0].add_widget(load_button)

            continue_button = Button(text=project)
            continue_buttoncallback = partial(start_main_software, project, True)
            continue_button.bind(on_release=continue_buttoncallback)
            continue_screen.children[0].add_widget(continue_button)


        load_screen.children[0].add_widget(get_go_back_button())
        continue_screen.children[0].add_widget(get_go_back_button())

        return kv
