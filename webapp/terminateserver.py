from flask import request
from data import DataCollector

shutdown_path = '/shutdown'


def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    DataCollector.tell_to_stop()
