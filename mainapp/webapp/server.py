from flask import Flask
from mainapp.webapp import application_manager


def start(project_name):
    server = Flask(__name__)

    application_manager.setupAppsOn(server, project_name)
    application_manager.openAllApps()

    server.run(host='0.0.0.0', debug=False)

    return "Server shut off"
