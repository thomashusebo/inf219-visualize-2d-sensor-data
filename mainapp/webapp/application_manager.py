from mainapp.webapp.apps.analysis_app import AnalysisApp
from mainapp.webapp.apps.live_app import LiveApp
from mainapp.webapp.apps.settings_app import SettingsApp
from mainapp.webapp.dataretriever import DataRetriever
import webbrowser as wb

apps = []


def setupAppsOn(server, project_name):
    live_data = DataRetriever(project_name)
    setup(
        app=LiveApp(url='/monitor/', load_on_server_start=True),
        server=server,
        data_manager=live_data,
        project_name=project_name
    )

    setup(
        app=AnalysisApp(url='/explore/', load_on_server_start=True),
        server=server,
        data_manager=live_data,
        project_name=project_name
    )

    setup(
        app=SettingsApp(url='/settings/', load_on_server_start=False),
        server=server,
        data_manager=live_data,
        project_name=project_name
    )


def setup(app, server, data_manager, project_name):
    app.setupOn(server, data_manager, project_name)
    apps.append(app)


def openAllApps():
    [wb.open('http://127.0.0.1:5000' + app.get_url()) for app in apps if app.load_on_server_start]
