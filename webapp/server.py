from flask import Flask
from webapp import applicationmanager


def start(project_name):
    server = Flask(__name__)

    applicationmanager.setupAppsOn(server, project_name)
    applicationmanager.openAllApps()

    server.run(debug=False)

    return "Server shut off"
