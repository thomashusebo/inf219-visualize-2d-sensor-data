import multiprocessing as mp

from data.DataCollector import DataCollector
from instrument_simulator import simulate_instrument_csv
from setupapp import setupapp
from webapp import server
from setupapp.setupapp import SetupApp


def name_qualifies(name):
    # TODO: Make more rigorous
    return name is not ""


if __name__ == '__main__':
    print("running setup")
    SetupApp().run()
    simulate_instrument_csv.run()
    data_collector = DataCollector(setupapp.name)
    data_collector.update(data_collector)
    server.start(setupapp.name)
''' if name_qualifies(setupapp.name):
    num_of_cores = 4
    data_collector = 
    jobs = []
    print("Creating pool")
    pool = mp.Pool(processes=num_of_cores)
    jobs.append(pool.apply_async(server.start, (setupapp.name,)))
    jobs.append(pool.apply_async(data_collector.update, (data_collector, setupapp.name)))
    jobs.append(pool.apply_async(simulate_instrument_csv,()))

    for job in jobs:
        job.get()'''

