from kivy.app import App
from kivy.uix.widget import Widget

name = ''
start_server = False


class Grid(Widget):
    pass


class SetupApp(App):

    def build(self):
        return Grid()


def exit_setup(instance):
    App.get_running_app().stop()


def on_text(instance, value):
    global name
    global start_server
    name = value
    start_server = True

    print(value, start_server)


def on_enter(instance, value):
    print('Enter textbox')
