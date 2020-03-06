import datetime
import dash
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from dataCollector import DataCollector
from factory import FigureCreator, HtmlCreator

# Gather data
data = []

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
        Output(component_id='heatmap-slider', component_property='max'),
    ],
    [
        Input('heatmap-slider', component_property='value'),
        Input('heatmap', component_property='clickData'),
        Input('interval-component', 'n_intervals')
    ])
def updateFigures(selectedIteration, clickData, n):
    # Collect data
    global data
    data = DataCollector.getData(data)
    numberOfFrames = len(data);

    # Find slider position/iteration to display in heatmap
    nextIteration = selectedIteration

    # Define iteration
    i = nextIteration

    # Define coordinate
    if clickData is not None:
        clickData = clickData['points'][0]
        coordinate = {'x': clickData['x'] - 1,
                      'y': clickData['y'] - 1}
    else:
        coordinate = {'x': 0, 'y': 0}

    # Define colormap
    zs = data[i]['zs']
    colorScale = ColorHandler.getColorScale(max_value=max(max(zs)),
                                            min_value=min(min(zs)))
    # Update figures
    heatmapFig = FigureCreator.getHeatMap(data, i, colorScale)
    lineChartFig = FigureCreator.getLineChart(data, i, coordinate, colorScale)

    return [heatmapFig,
            lineChartFig,
            html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
            numberOfFrames]


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
