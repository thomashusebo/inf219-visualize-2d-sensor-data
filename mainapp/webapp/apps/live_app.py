import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

from mainapp.webapp.apps.abstract_app import AbstractApp
from mainapp.termination.termination import shutdown_path, shutdown_server
from mainapp.webapp.figures import heatmap
from mainapp.webapp.colors import color_manager

#stylesheet = None
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class LiveApp(AbstractApp):
    def setupOn(self, server, data_manager):
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
                className='seven columns'
            ),
            dcc.RadioItems(
                id='map_chooser',
                options=[
                    {'label': 'Heatmap', 'value': 'heatmap'},
                    {'label': 'Contour', 'value': 'contour'},
                    {'label': 'Surface', 'value': 'surface'}
                ],
                value='heatmap',
                className ='seven columns',
                labelStyle={'display': 'inline-block'}
            )
        ])

        @live_app.callback(dash.dependencies.Output("hidden_div", "children"),
                           [dash.dependencies.Input('url', 'pathname')])
        def shutdown(pathname):
            if pathname == shutdown_path:
                shutdown_server()
                return dcc.Location(pathname="/", id="someid_doesnt_matter")

        # Define callbacks
        @live_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='live-clock', component_property='children')
            ],
            [
                Input('interval-component', 'n_intervals'),
                Input('map_chooser', 'value')
            ])
        def updateFigures(nIntervals, plot_type):
            # Collect data
            last_timestamp, heatmap_data = data_manager.get_heatmap_data(data_manager, live=True)

            # Define colormap
            colorScale = color_manager.getColorScale()

            # Update figures
            heatmapFig = heatmap.getHeatMap(heatmap_data, last_timestamp, colorScale, plot_type)

            return [
                heatmapFig,
                html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
            ]
