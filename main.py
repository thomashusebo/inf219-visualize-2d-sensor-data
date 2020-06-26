from mainapp import multiprocess_manager
from mainapp.instrument_simulator import simulate_instrument_csv


def name_qualifies(name):
    # TODO: Make more rigorous
    return name is not ""


def main():
    setup = SetupApp()
    setup.run()

    if name_qualifies(setupapp.name):
        multiprocess_manager.start(project_name=setupapp.name)


if __name__ == '__main__':
    # Imports are put here to avoid multiprocessing to open a kivy application window per multiprocess
    from setupapp import setupapp
    from setupapp.setupapp import SetupApp
    main()
