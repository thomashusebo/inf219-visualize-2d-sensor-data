import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

from webapp.apps.AbstractApp import AbstractApp
from webapp.terminateserver import shutdown_path, shutdown
from webapp.figures import heatmap
from webapp.colorHandler import ColorHandler
from webapp.dataCollector import DataCollector

stylesheet = None
# stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
projectName = "200308Test002SmallTankObstructedFlow_simulation"
data = []


class LiveApp(AbstractApp):
    def setupOn(self, server):
        live_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        live_app.layout = html.Div([
            # Page Header
            html.H1('Live View'),
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
            html.Div([
                dcc.Markdown('''
                    ##### Description
                    For this experiment we filled the tank only tapwater. 

                    ##### Logg
                    - Added tapwater 
                        -   then measurements (1-5)
                    - Added solution tapwater with conditor into (2.5, 1.5)
                        -   then measurements (6-11)
                    - Added solution tapwater w/0.23M NaCl, into (2.5, 1.5)
                        -   then measurements (12-20)
                    - Added solution tapwater w/0.90M NaCl, into (0.0, 1.5)
                        -   then measurements (21-27)


                    ''')
            ],
                className='four columns'
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
        ])

        @live_app.callback(dash.dependencies.Output("hidden_div", "children"),
                           [dash.dependencies.Input('url', 'pathname')])
        def shutdown_server(pathname):
            if pathname == shutdown_path:
                shutdown()
                return dcc.Location(pathname="/", id="someid_doesnt_matter")

        # Define callbacks
        @live_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='live-clock', component_property='children')
            ],
            [
                Input('interval-component', 'n_intervals')
            ])
        def updateFigures(nIntervals):
            # Collect data
            global data
            data = DataCollector.getData(data, projectName)

            nextIteration = len(data) - 1

            # Define colormap
            colorScale = ColorHandler.getColorScale()

            # Update figures
            heatmapFig = heatmap.getHeatMap(data, nextIteration, colorScale)

            return [
                heatmapFig,
                #"",
                html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
            ]
