import multiprocessing as mp
import time

from data import data_collector
from instrument_simulator import simulate_instrument_csv
from setupapp import setupapp
from webapp import server
from setupapp.setupapp import SetupApp


def name_qualifies(name):
    # TODO: Make more rigorous
    return name is not ""


if __name__ == '__main__':
    if setupapp.name == '':

        SetupApp().run()

        if name_qualifies(setupapp.name):
            num_of_cores = 4
            simulate_instrument = False

            jobs = []
            pool = mp.Pool(processes=num_of_cores)

            if simulate_instrument:
                jobs.append(pool.apply_async(simulate_instrument_csv.run, ()))
            jobs.append(pool.apply_async(data_collector.update, (setupapp.name,)))
            jobs.append(pool.apply_async(server.start, (setupapp.name,)))

            for job in jobs:
                while not job.ready():
                    time.sleep(2)
                    pass
                if job.successful():
                    print(job.get())
