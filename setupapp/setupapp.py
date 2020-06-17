from kivy.app import App
import kivy.uix.button as kb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

name = ''
start_server = False


class SetupApp(App):

    def build(self):
        root = BoxLayout(
            orientation='vertical',
            padding=[100, 75, 100, 75],
            spacing=10,
        )

        project_name = TextInput(text='Input project name')
        project_name.bind(on_text_validate=on_enter)
        project_name.bind(text=on_text)

        btn1 = kb.Button(text='Start server')
        btn1.bind(on_press=exit_setup)

        root.add_widget(project_name)
        root.add_widget(btn1)

        return root


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
