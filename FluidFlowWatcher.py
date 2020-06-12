from webapp import webapp
from setupapp import setupapp

if __name__ == '__main__':
    setupapp.SetupApp().run()

print("Widget done")
webapp.startServer()
print("done")