from webapp import liveApp, compareApp, temporalApp
import webbrowser as wb

apps = []


def setupAppsOn(server):
    liveApp.setupOn(server)
    apps.append(liveApp)

    compareApp.setupOn(server)
    apps.append(compareApp)

    temporalApp.setupOn(server)
    apps.append(temporalApp)


def openAllApps():
    [wb.open('http://127.0.0.1:5000' + app.url) for app in apps]