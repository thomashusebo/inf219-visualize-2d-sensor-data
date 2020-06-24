from flask import request
from data import data_collector

shutdown_path = '/shutdown'


def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    data_collector.tell_to_stop()
