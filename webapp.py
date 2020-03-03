import datetime
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from factory import FigureCreator, HtmlCreator

# Heatmap data
n = 14  # number of columns
m = 7  # number of rows
xs = [i for i in range(1, n + 1)]  # Defines x's
ys = [i for i in range(1, m + 1)]  # Defines y's
zs = [[i * j for i in xs] for j in ys]  # Defines plotted value in heatmap, product of x and y

# Linechart data
line_xs = [i for i in range(30)]
line_ys = [(-1) ** i * i ** 2 + i ** 2 + (i / 2) ** 2 for i in line_xs]

# Define color scale
color_scale = ColorHandler.getColorScale(max_value=max(max(zs)),
                                         min_value=min(min(zs)))

# Define figures
heatmap_fig, color_scale = FigureCreator.getHeatMap(xs, ys, zs, color_scale)
linechart_fig = FigureCreator.getLineChart(line_xs, line_ys, color_scale)

# Setup HTML and CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)

appContent = {'heatmap':heatmap_fig,
              'linechart':linechart_fig}

HtmlCreator.setup(app, appContent)

@app.callback(Output('live-clock', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    return [
        html.Span(datetime.datetime.now().strftime("%H:%M:%S"))
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
