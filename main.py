from setupapp import setupapp2
from webapp import server
from setupapp.setupapp2 import SetupApp


def name_qualifies(name):
    # TODO: Make more rigorous
    return name is not ""


if __name__ == '__main__':
    SetupApp().run()

if name_qualifies(setupapp2.name):
    server.start(setupapp2.name)
