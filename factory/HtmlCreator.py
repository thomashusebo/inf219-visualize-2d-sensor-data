import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html


def setup(app):
    app.layout = html.Div([
        # Title
        html.Div([
            html.H1("INF219 Visualization of 2d sensor data")
        ]),

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
                      ),
        ],
            className='seven columns'
        ),

        # Line chart
        html.Div([
            dcc.Graph(id='linechart',
                      config={
                          "displaylogo": False,
                          "modeBarButtonsToRemove": []
                      }),
        ],
            className='four columns'
        ),

        # Slider
        html.Div([
            daq.Slider(
                id='heatmap-slider',
                min=0,
                value=0,
                max=6,
                color='black'
            )
        ],
            className='seven columns'

        ),
    ])

    return None
