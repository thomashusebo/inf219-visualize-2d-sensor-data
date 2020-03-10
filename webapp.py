import datetime
import dash
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from dataCollector import DataCollector
from factory import FigureCreator, HtmlCreator

# Gather data
data = []
projectName = "200308Test001SmallTankFreeFlow_simulation"

# Setup the web application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
HtmlCreator.setup(app)


# Define callbacks
@app.callback(
    [
        Output(component_id='heatmap', component_property='figure'),
        Output(component_id='linechart', component_property='figure'),
        Output(component_id='live-clock', component_property='children'),
        Output(component_id='heatmap-slider', component_property='max')
    ],
    [
        Input('heatmap-slider', component_property='value'),
        Input('heatmap', component_property='clickData'),
        Input('interval-component', 'n_intervals'),
        Input('play-button', 'on'),

    ])
def updateFigures(selectedIteration, clickData, n, playModeOn):
    # Collect data
    global data
    data = DataCollector.getData(data, projectName)
    numberOfFrames = len(data)

    # Ensures that we avoid index out of bounds exceptions when accessing data
    if selectedIteration > numberOfFrames-1:
        selectedIteration = -1

    # Find slider position/iteration to display in heatmap
    if playModeOn:
        nextIteration = numberOfFrames-1
    else:
        nextIteration = selectedIteration-1

    # Define coordinate
    if clickData is not None:
        clickData = clickData['points'][0]
        coordinate = {'x': clickData['x'] - 1,
                      'y': clickData['y'] - 1}
    else:
        coordinate = {'x': 0, 'y': 0}

    # Define colormap
    colorScale = ColorHandler.getColorScale()

    # Update figures
    heatmapFig = FigureCreator.getHeatMap(data, nextIteration, colorScale)
    lineChartFig = FigureCreator.getLineChart(data, nextIteration, coordinate, colorScale)

    return [
        heatmapFig,
        lineChartFig,
        "",
        #html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
        numberOfFrames-1,
        ]


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
