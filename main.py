from webapp import server
from setupapp.setupapp import SetupApp

project_name = "200308Test002SmallTankObstructedFlow_simulation"

if __name__ == '__main__':
    SetupApp().run()

server.start(project_name)