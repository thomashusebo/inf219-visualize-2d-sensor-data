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
    [Output('heatmap', 'figure'),
     Output('linechart', 'figure'),
     Output('live-clock', 'children')],
    [Input('heatmap-slider', 'value'),
     Input('heatmap', 'clickData'),
     Input('interval-component', 'n_intervals')])
def updateFigures(selected_iteration, clickData, n):
    global data
    data = DataCollector.getData(data)
    # Define iteration
    i = selected_iteration

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
            html.Span(datetime.datetime.now().strftime("%H:%M:%S"))]


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
