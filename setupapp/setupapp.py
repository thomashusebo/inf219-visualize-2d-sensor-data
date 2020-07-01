from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from storage.database_manager import DatabaseManager
from bcrypt import hashpw, gensalt
import numpy as np

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
        project_name = self.project_name.text
        salt = gensalt()
        password = hashpw(self.password.text.encode('utf-8'), salt)
        confirm_password = hashpw(self.confirm_password.text.encode('utf-8'), salt)

        if password != confirm_password:
            self.status_label.text = 'Passwords did not match \n' \
                                     'Please try again'.format(project_name)
            return

        if database_manager.try_to_add_new_project_name(project_name, password):
            global active_project, datacollection
            active_project = project_name
            datacollection = True
            App.get_running_app().stop()
        else:
            self.status_label.text = 'Project name "{}" found in database \n' \
                                     'Please choose a different project name'.format(project_name)


class ContinueProjectWindow(Screen):
    pass


class LoadProjectWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


def start_main_software(project, collect_data, instance):
    global active_project, datacollection
    active_project = project
    datacollection = collect_data
    App.get_running_app().stop()


def return_to_main(instance):
    App.get_running_app().root.transition = SlideTransition(direction='right')
    App.get_running_app().root.current = 'main'


def get_go_back_button():
    go_back_button = Button(text="Go Back", height=40)
    go_back_button.bind(on_release=return_to_main)
    return go_back_button


class SetupApp(App):

    def build(self):
        kv = Builder.load_file("setupapp\\setup.kv")
        load_screen = kv.get_screen("load_project")
        load_button_grid = GridLayout(cols=1, size_hint_y=None)
        load_button_grid.bind(minimum_height=load_button_grid.setter('height'))
        load_scrollview = ScrollView(size_hint=(1,1), do_scroll_y=True)

        continue_screen = kv.get_screen("continue_project")
        continue_button_grid = GridLayout(cols=1, size_hint_y=None)
        continue_button_grid.bind(minimum_height=continue_button_grid.setter('height'))
        continue_scrollview = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        projects = database_manager.get_projects()
        for project in sorted(projects):
            load_button = Button(text=project,size_hint_y=None, height=40)
            load_buttoncallback = partial(start_main_software, project, False)
            load_button.bind(on_release=load_buttoncallback)
            load_button_grid.add_widget(load_button)

            continue_button = Button(text=project,size_hint_y=None, height=40)
            continue_buttoncallback = partial(start_main_software, project, True)
            continue_button.bind(on_release=continue_buttoncallback)
            continue_button_grid.add_widget(continue_button)

        load_scrollview.add_widget(load_button_grid)
        load_screen.children[0].add_widget(load_scrollview)
        load_screen.children[0].add_widget(get_go_back_button())

        continue_scrollview.add_widget(continue_button_grid)
        continue_screen.children[0].add_widget(continue_scrollview)
        continue_screen.children[0].add_widget(get_go_back_button())

        return kv
