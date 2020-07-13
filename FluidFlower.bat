ECHO Starting FluidFlower...
ECHO Creating directories ignored by git
mkdir storage\databases
mkdir incoming_data
mkdir mainapp\termination\stop_dir
mkdir export
ECHO Starting Application...
python -m pipenv run python main.py