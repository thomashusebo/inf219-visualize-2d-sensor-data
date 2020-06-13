import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

from webapp.apps.AbstractApp import AbstractApp
from webapp.terminateserver import shutdown_path, shutdown

stylesheet = None
#stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class TemporalApp(AbstractApp):
    def setupOn(self, server):
        temporal_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        temporal_app.layout = html.Div([
            # Page header
            html.H1('Temporal View'),
            dcc.Location(id='url', refresh=False),
            html.Div(id="hidden_div"),
            dcc.Link('Shutdown server', href=shutdown_path),

            # Title
            html.Div([
                dcc.Markdown('''
                   ## Reconstruction of SmallTankTest001: Free Flow
                   #### One new measurement per second, regardless of measurement timestamp
                   ''')
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
                          ),
            ],
                className='three columns'
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
                daq.BooleanSwitch(
                    id='play-button',
                    on=True
                ),
                daq.Slider(
                    id='heatmap-slider',
                    min=1,
                    value=1,
                    max=1,
                    color='black',
                    handleLabel={"showCurrentValue": True, "label": "Iteration"},
                    size=0,
                ),

            ],
                className='three columns'
            ),
        ])

        @temporal_app.callback(dash.dependencies.Output("hidden_div", "children"),
                               [dash.dependencies.Input('url', 'pathname')])
        def shutdown_server(pathname):
            if pathname == shutdown_path:
                shutdown()
                return dcc.Location(pathname="/", id="someid_doesnt_matter")
