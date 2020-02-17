import datetime
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from dash.dependencies import Input, Output
from colorHandler import ColorHandler as colors

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

####################################################
## Setup a heatmap data
n = 14                                  # number of columns
m = 7                                   # number of rows
xs = [i for i in range(1,n+1)]          # Defines x's
ys = [i for i in range(1, m+1)]         # Defines y's
zs = [[i * j for i in xs] for j in ys]  # Defines plotted value in heatmap

# Create heatmap figure used in app from data and layout
color_scale = colors.getColorScale(max_value=max(max(zs)),
                                   min_value=min(min(zs)))

heatmap_data = go.Heatmap(x=xs,
                          y=ys,
                          z=zs,
                          colorscale=color_scale
                          )
heatmap_layout = go.Layout(title=go.layout.Title(text='Heatmap Title'))

heatmap_fig = {
    'data':[heatmap_data],
    'layout':heatmap_layout}
###################################################

###########################################
## Setup a line chart data
x = [i for i in range(30)]
y = [(-1)**i*i**2+i**2+(i/2)**2 for i in x]


# Create line chart figure used in app from data and layout
linechart_data = go.Scatter(x=x,
                            y=y,
                            name="Close",
                            line=dict(color=color_scale[0][1])
                            )
linechart_layout = go.Layout(title=go.layout.Title(text="Line chart"))
linechart_fig = {
    'data':[linechart_data],
    'layout':linechart_layout
}
###########################################


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
           interval = 1*1000, #milliseconds
           n_intervals = 0
       )
    ]),

    # Heatmap
    html.Div([
        dcc.Graph(id='heatmap',
                  config = {
                      "displaylogo":False,
                      "modeBarButtonsToRemove":['zoom2d']
                  },
                  figure=heatmap_fig
                  )
        ],
        className='seven columns'
    ),

    # Line chart
    html.Div([
        dcc.Graph(id='linechart',
                  config = {
                      "displaylogo":False,
                      "modeBarButtonsToRemove":[]
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


if __name__ =='__main__':
    app.run_server(debug=True)