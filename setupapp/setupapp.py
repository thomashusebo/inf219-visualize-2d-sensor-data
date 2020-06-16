from kivy.app import App
import kivy.uix.button as kb
from kivy.uix.widget import Widget


class ButtonWidget(Widget):

    def __init__(self, **kwargs):
        super(ButtonWidget, self).__init__(**kwargs)
        self.ButtonStartServer = kb.Button(text='Start Server')
        self.ButtonStartServer.bind(on_press=exit_setup)
        self.add_widget(self.ButtonStartServer)


class SetupApp(App):

    def build(self):
        return ButtonWidget()


def exit_setup(instance):
    App.get_running_app().stop()
