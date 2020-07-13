from mainapp import multiprocess_manager
from mainapp.instrument_simulator import simulate_instrument_csv


def main():
    setup = SetupApp()
    setup.run()

    if setupapp.active_project is not "":
        multiprocess_manager.start(project_name=setupapp.active_project,
                                   datacollection=setupapp.datacollection,
                                   #instrument_simulator=simulate_instrument_csv
        )


if __name__ == '__main__':
    # Imports are put here to avoid each process to open a kivy application window
    from setupapp import setupapp
    from setupapp.setupapp import SetupApp
    main()
