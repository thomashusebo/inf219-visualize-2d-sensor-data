import datetime
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from colorHandler import ColorHandler
from figureCreator import FigureCreator

# Heatmap data
n = 14  # number of columns
m = 7  # number of rows
xs = [i for i in range(1, n + 1)]  # Defines x's
ys = [i for i in range(1, m + 1)]  # Defines y's
zs = [[i * j for i in xs] for j in ys]  # Defines plotted value in heatmap, product of x and y
color_scale = ColorHandler.getColorScale(max_value=max(max(zs)),
                                         min_value=min(min(zs)))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
heatmap_fig, color_scale = FigureCreator.getHeatMap(xs, ys, zs, color_scale)
linechart_fig = FigureCreator.getLineChart(color_scale)

app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
    # Title
    html.Div([
        html.H1("INF219 Visualization of 2d sensor data")
    ],
    ),

    # Time
    html.Div([
        html.Div(id='live-clock'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # milliseconds
            n_intervals=0
        )
    ]),

    # Heatmap
    html.Div([
        dcc.Graph(id='heatmap',
                  config={
                      "displaylogo": False,
                      "modeBarButtonsToRemove": ['zoom2d']
                  },
                  figure=heatmap_fig
                  )
    ],
        className='seven columns'
    ),

    # Line chart
    html.Div([
        dcc.Graph(id='linechart',
                  config={
                      "displaylogo": False,
                      "modeBarButtonsToRemove": []
                  },
                  figure=linechart_fig)
    ],
        className='four columns'
    ),

    # Slider
    html.Div([
        daq.Slider(
            id='heatmap slider',
            min=0,
            value=50,
            max=100,
            color='black'
        )
    ],
        className='seven columns'

    ),
])


@app.callback(Output('live-clock', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    return [
        html.Span(datetime.datetime.now().strftime("%H:%M:%S"))
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
