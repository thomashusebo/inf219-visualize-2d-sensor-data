import time
import multiprocessing as mp
from mainapp.data import data_collector
from mainapp.webapp import server


def start(project_name, cpu_cores=None, instrument_simulator=None):

    pool = mp.Pool(processes=cpu_cores)
    jobs = []
    if cpu_cores is None: cpu_cores = mp.cpu_count()

    if instrument_simulator is not None:
        if cpu_cores < 3:
            raise Exception("Need at least 3 cpu cores to run with simulating instrument. \n"
                            "1 for instrument, 1 for data collector, 1 for instrument simulator\n"
                            "Cores given access to: {}".format(cpu_cores))
        jobs.append(pool.apply_async(instrument_simulator.run, (1,)))

    if cpu_cores < 2:
        raise Exception("Need at least 2 cpu cores run application. \n"
                        "1 for instrument, 1 for data collector\n"
                        "Cores given access to: {}".format(cpu_cores))
    jobs.append(pool.apply_async(data_collector.update, (project_name,)))
    jobs.append(pool.apply_async(server.start, (project_name,)))

    for job in jobs:
        while not job.ready():
            time.sleep(2)
        if job.successful():
            print(job.get())