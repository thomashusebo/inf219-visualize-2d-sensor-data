# Visualize live sensor data
This project is part of bachelor degree in Informatics, Data Science, at University of Bergen. 

## About the project
An ongoing collaboration between Department of Physics and Technology (IFT), Department of Earth Science, and Department of 
Mathematics at UiB are currently working on creating the second iteration of a fluid-flow-rig. The fluid-flow-rig is a 
physical tank used to study fluid flow and convection patterns.

Sensors will be placed on the fluid-flow-rig, providing real-time resistivity readings. Because of the number of 
sensors, frequency of data, and duration per intended fluid-flow-rig project, a visualization of the data is very 
useful. 

My project will provide the functionality that enables the user to inspect both the live data, and previous readings in
an ongoing project.

## More information
See the [wiki](https://github.com/thomashusebo/inf219-visualize-2d-sensor-data/wiki)

## Installation
1. Install python 3.7.6
1. Clone repository
1. Install dependencies: 

Recommended:
> - Install pipenv
> - Run batch script FluidFlower.bat 

> The batch file will create a virtual environment based on the pip files. If this is the first time to set up, this will install all necessary dependencies. The batch script also creates subdirectories ignored by git.

Not recommended:
> - Manually install dependencies from requirements.txt or pip files. 
> - Manually add directories ignored by git (see batch file)

4. Start software: FluidFlower.bat or run main.py

## File format
See [wiki/File-Format](https://github.com/thomashusebo/inf219-visualize-2d-sensor-data/wiki/File-Format)

## Prototype
Before the corona lockdown, a prototype of the software where working (though with manually feeding input to a 
file-creator). The code for the protype is available [here](https://github.com/thomashusebo/inf219-visualize-2d-sensor-data/tree/prototype). 
However, the data and 
the file-creators are not included. For the curious, here is a [video of the prototype testing](https://vimeo.com/396326719)

