import os
from flask import request
from mainapp.data import data_collector
from mainapp.instrument_simulator import simulate_instrument_csv

shutdown_path = '/shutdown'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    simulate_instrument_csv.tell_to_stop()
    data_collector.tell_to_stop()


def time_to_stop(stopping_dir, stopping_file):
    files = next(os.walk(stopping_dir))[2]
    if stopping_file in files:
        os.remove(stopping_dir + '\\' + stopping_file)
        return True
    return False


def clean_up_stopping_dir(stopping_dir, stopping_file):
    files = next(os.walk(stopping_dir))[2]
    for file in files:
        if file == stopping_file:
            os.remove(stopping_dir + '\\' + stopping_file)

