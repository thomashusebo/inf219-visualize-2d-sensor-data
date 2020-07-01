import multiprocessing as mp
from mainapp.data import data_collector
from mainapp.webapp import server


def number_of_required_cores(datacollection, instrument_simulator):
    num = 1
    if datacollection:
        num += 1
    if instrument_simulator is not None:
        num += 1
    return num


def start(project_name, cpu_cores=None, datacollection=False, instrument_simulator=None):

    pool = mp.Pool(processes=cpu_cores)
    jobs = []
    if cpu_cores is None: cpu_cores = mp.cpu_count()

    required_cores = number_of_required_cores(datacollection, instrument_simulator)

    if cpu_cores < required_cores:
        raise Exception("Need at least {} cores to run on correct setting. Only found {} cores".format(
            required_cores, cpu_cores
        ))

    # Append jobs
    if datacollection:
        jobs.append(pool.apply_async(data_collector.update, (project_name,)))
    if instrument_simulator is not None:
        jobs.append(pool.apply_async(instrument_simulator.run, (1,)))
    jobs.append(pool.apply_async(server.start, (project_name,)))

    for job in jobs:
        #while not job.ready():
        #    time.sleep(2)
        #if job.successful():
        print(job.get())