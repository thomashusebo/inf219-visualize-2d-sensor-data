from setupapp import setupapp
from webapp import server
from setupapp.setupapp import SetupApp


def name_qualifies(name):
    # TODO: Make more rigorous
    return name is not ""


if __name__ == '__main__':
    SetupApp().run()

if name_qualifies(setupapp.name):
    server.start(setupapp.name)
