from kivy.app import App
import kivy.uix.button as kb
from kivy.uix.widget import Widget

class Button_Widget(Widget):

    def __init__(self, **kwargs):
        super(Button_Widget, self).__init__(**kwargs)
        self.btn1 = kb.Button(text='Start Server')
        self.btn1.bind(on_press=self.callback)
        self.add_widget(self.btn1)


    def callback(self, instance):
        App.get_running_app().stop()

class MyApp(App):

    def build(self):
        return Button_Widget()

#if __name__ == '__main__':
#    MyApp().run()

