from setupapp import setupapp
from webapp import server
from setupapp.setupapp import SetupApp

#project_name = "200308Test002SmallTankObstructedFlow_simulation"
#start_server = False

if __name__ == '__main__':
    SetupApp().run()

if setupapp.start_server:
    server.start(setupapp.name)