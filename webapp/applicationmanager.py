from webapp.apps.LiveApp import LiveApp
from webapp.apps.CompareApp import CompareApp
from webapp.apps.TemporalApp import TemporalApp
import webbrowser as wb

apps = []


def setupAppsOn(server):
    setup(
        app=LiveApp(url='/liveapp/', load_on_server_start=True),
        server=server)

    setup(
        app=CompareApp(url='/compareapp/', load_on_server_start=True),
        server=server)

    setup(
        app=TemporalApp(url='/temporalapp/', load_on_server_start=True),
        server=server)


def setup(app, server):
    app.setupOn(server)
    apps.append(app)


def openAllApps():
    [wb.open('http://127.0.0.1:5000' + app.get_url()) for app in apps if app.load_on_server_start]
