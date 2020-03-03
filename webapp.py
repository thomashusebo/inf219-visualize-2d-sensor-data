import datetime
import dash
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from dataCollector import DataCollector
from factory import FigureCreator, HtmlCreator

# Heatmap data
data = DataCollector.getData()
iterationID = 5
oneFrame = data[iterationID]
xs = oneFrame['xs']
ys = oneFrame['ys']
zs = oneFrame['zs']

# Linechart data
line_xs = [i for i in range(len(data))]
line_ys = [data[i]['zs'][0][0] for i in range(len(data))]

# Define color scale
color_scale = ColorHandler.getColorScale(max_value=max(max(zs)),
                                         min_value=min(min(zs)))

# Define figures
heatmap_fig = FigureCreator.getHeatMap(xs, ys, zs, color_scale)
linechart_fig = FigureCreator.getLineChart(line_xs, line_ys, color_scale)
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
