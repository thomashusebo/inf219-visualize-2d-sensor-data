from kivy.app import App
import kivy.uix.button as kb
from kivy.uix.widget import Widget


class ButtonWidget(Widget):

    def __init__(self, **kwargs):
        super(ButtonWidget, self).__init__(**kwargs)
        self.btn1 = kb.Button(text='Start Server')
        self.btn1.bind(on_press=callback)
        self.add_widget(self.btn1)


class MyApp(App):

    def build(self):
        return ButtonWidget()


def callback(instance):
    App.get_running_app().stop()
