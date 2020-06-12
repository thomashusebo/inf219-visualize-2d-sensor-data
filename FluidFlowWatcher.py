from webapp import server
from setupapp import setupapp

if __name__ == '__main__':
    setupapp.SetupApp().run()

server.start()