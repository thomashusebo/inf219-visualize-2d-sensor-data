import datetime
import dash
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from dataCollector import DataCollector
from factory import FigureCreator, HtmlCreator

# Gather data
data = DataCollector.getData()

# Define which measurement iteration to show in heatmap
iterationID = 6

# Define which coordinate to show data in linechart
coordinate = {'x': 6, 'y': 6}

# Define colormap
zs = data[iterationID]['zs']
color_scale = ColorHandler.getColorScale(max_value=max(max(zs)),
                                         min_value=min(min(zs)))

# Define figures
heatmap_fig = FigureCreator.getHeatMap(data, iterationID, color_scale)
linechart_fig = FigureCreator.getLineChart(data, iterationID, coordinate, color_scale)
appContent = {'heatmap': heatmap_fig,
              'linechart': linechart_fig}

# Setup the web application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
HtmlCreator.setup(app, appContent)


# Define callbacks
@app.callback(Output('live-clock', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    return [
        html.Span(datetime.datetime.now().strftime("%H:%M:%S"))
    ]


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
