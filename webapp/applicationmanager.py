from webapp import liveApp, compareApp, temporalApp
import webbrowser as wb


def setupAppsOn(server):
    liveApp.setupOn(server)
    compareApp.setupOn(server)
    temporalApp.setupOn(server)


def openAllApps():
    wb.open('http://127.0.0.1:5000' + liveApp.url)
    wb.open('http://127.0.0.1:5000' + compareApp.url)
    wb.open('http://127.0.0.1:5000' + temporalApp.url)
