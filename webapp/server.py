from flask import Flask
from webapp import applicationmanager


def start():
    server = Flask(__name__)

    applicationmanager.setupAppsOn(server)
    applicationmanager.openAllApps()

    server.run(debug=False)
