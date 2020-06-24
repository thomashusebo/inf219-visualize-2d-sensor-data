from webapp.apps.live_app import LiveApp
from webapp.apps.compare_app import CompareApp
from webapp.apps.temporal_app import TemporalApp
import webbrowser as wb
from data.data_manager import DataManager

apps = []


def setupAppsOn(server, project_name):
    live_data = DataManager(project_name)
    setup(
        app=LiveApp(url='/liveapp/', load_on_server_start=True),
        server=server,
        data_manager=live_data)

    setup(
        app=CompareApp(url='/compareapp/', load_on_server_start=True),
        server=server,
        data_manager=live_data)

    setup(
        app=TemporalApp(url='/temporalapp/', load_on_server_start=True),
        server=server,
        data_manager=live_data)


def setup(app, server, data_manager):
    app.setupOn(server, data_manager)
    apps.append(app)


def openAllApps():
    [wb.open('http://127.0.0.1:5000' + app.get_url()) for app in apps if app.load_on_server_start]
