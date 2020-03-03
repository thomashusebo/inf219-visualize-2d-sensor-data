import datetime

import dash
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from dataCollector import DataCollector
from factory import FigureCreator, HtmlCreator

# Gather data
data = DataCollector.getData()

# Define which coordinate to show data in linechart
coordinate = {'x': 6, 'y': 6}

# Setup the web application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
HtmlCreator.setup(app)


# Define callbacks
@app.callback(Output('live-clock', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    return [
        html.Span(datetime.datetime.now().strftime("%H:%M:%S"))
    ]


@app.callback(
    [Output('heatmap', 'figure'),
     Output('linechart', 'figure')],
    [Input('heatmap-slider', 'value')])
def update_figure(selected_iteration):
    # Gather data
    thisData = data[selected_iteration]

    # Define colormap
    zs = thisData['zs']
    thisColorScale = ColorHandler.getColorScale(max_value=max(max(zs)),
                                                min_value=min(min(zs)))
    # Update figures
    thisHeatmapFig = FigureCreator.getHeatMap(data, selected_iteration, thisColorScale)
    thisLineChartFig = FigureCreator.getLineChart(data, selected_iteration, coordinate, thisColorScale)

    return [thisHeatmapFig, thisLineChartFig]


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
