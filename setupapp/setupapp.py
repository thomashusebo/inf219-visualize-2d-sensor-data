from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from storage.project_manager import ProjectManager
from bcrypt import hashpw, gensalt
import numpy as np

active_project = ''
project_manager = ProjectManager()
datacollection = False


class MainWindow(Screen):
    @staticmethod
    def quit():
        App.get_running_app().stop()


class NewProjectWindow(Screen):
    project_name = ObjectProperty(None)

    def start_new_project(self):
        project_name = self.project_name.text
        height = int(self.pixel_height.text)
        width = int(self.pixel_width.text)
        salt = gensalt()
        min_length = 4
        if len(self.password.text) < min_length:
            self.status_label.text = 'Passwords had less than {} characters \n' \
                                     'Please use a longer password'.format(min_length, project_name)
            return
        password = hashpw(self.password.text.encode('utf-8'), salt)
        confirm_password = hashpw(self.confirm_password.text.encode('utf-8'), salt)

        if password != confirm_password:
            self.status_label.text = 'Passwords did not match \n' \
                                     'Please try again'.format(project_name)
            return

        if height < 0 or height > 99 or width < 0 or width > 99:
            self.status_label.text = 'Pixels height/width must be in [0,99] \n' \
                                     'Please try again'.format(project_name)
            return


        if project_manager.try_to_add_new_project_name(project_name, password, height, width):
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


class ExportProjectWindow(Screen):
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


def export_project(project_name, instance):
    project_manager.export_project(project_name)
    pass


class SetupApp(App):

    def build(self):
        kv = Builder.load_file("setupapp\\setup.kv")
        load_screen = kv.get_screen("load_project")
        load_button_grid = GridLayout(cols=1, size_hint_y=None)
        load_button_grid.bind(minimum_height=load_button_grid.setter('height'))
        load_scrollview = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        continue_screen = kv.get_screen("continue_project")
        continue_button_grid = GridLayout(cols=1, size_hint_y=None)
        continue_button_grid.bind(minimum_height=continue_button_grid.setter('height'))
        continue_scrollview = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        export_screen = kv.get_screen("export_project")
        export_button_grid = GridLayout(cols=1, size_hint_y=None)
        export_button_grid.bind(minimum_height=export_button_grid.setter('height'))
        export_scrollview = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        projects = project_manager.get_projects()
        for project in sorted(projects):
            load_button = Button(text=project, size_hint_y=None, height=40)
            load_buttoncallback = partial(start_main_software, project, False)
            load_button.bind(on_release=load_buttoncallback)
            load_button_grid.add_widget(load_button)

            continue_button = Button(text=project, size_hint_y=None, height=40)
            continue_buttoncallback = partial(start_main_software, project, True)
            continue_button.bind(on_release=continue_buttoncallback)
            continue_button_grid.add_widget(continue_button)

            export_button = Button(text=project, size_hint_y=None, height=40)
            export_buttoncallback = partial(export_project, project)
            export_button.bind(on_release=export_buttoncallback)
            export_button_grid.add_widget(export_button)

        load_scrollview.add_widget(load_button_grid)
        load_screen.children[0].add_widget(load_scrollview)
        load_screen.children[0].add_widget(get_go_back_button())

        continue_scrollview.add_widget(continue_button_grid)
        continue_screen.children[0].add_widget(continue_scrollview)
        continue_screen.children[0].add_widget(get_go_back_button())

        export_scrollview.add_widget(export_button_grid)
        export_screen.children[0].add_widget(export_scrollview)
        export_screen.children[0].add_widget(get_go_back_button())

        return kv
