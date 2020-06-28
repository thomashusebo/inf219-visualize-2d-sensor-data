import datetime
import hashlib

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State

from mainapp.webapp.apps.abstract_app import AbstractApp
from mainapp.termination.termination import shutdown_path, shutdown_server
from mainapp.webapp.figures import heatmap
from mainapp.webapp.colors import color_manager

# stylesheet = None
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
log = ""
encrypted_project_password = hashlib.sha256("passord123".encode()).hexdigest()


class LiveApp(AbstractApp):
    def setupOn(self, server, data_manager):
        live_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        live_app.layout = html.Div([
            # Page Header
            html.Div([
                html.H1('Live View'),
                dcc.Location(id='url', refresh=False),
                html.Div(id="hidden_div"),
                dcc.Link('Shutdown server', href=shutdown_path),

                # Time
                html.Div([
                    html.Div(id='live-clock'),
                    dcc.Interval(
                        id='interval-component',
                        interval=1 * 1000,  # milliseconds
                        n_intervals=0
                    )
                ]),
            ]),

            # Log
            html.Div([
                dcc.Markdown(
                    children='''##### Log'''),
                html.Div(
                    id='log',
                    style={'whiteSpace': 'pre-line'},
                    children=dcc.Markdown(log)),
                dcc.Textarea(
                    id='log-entry',
                    style={'width': '100%', 'height': 50},
                    placeholder='Enter log entry...'
                ),
                dcc.Input(
                    id="project-password",
                    type='password',
                    placeholder="Enter project password...",
                ),
                html.Button('Submit', id='submit-log-entry', n_clicks=0),

            ],
                className='four columns'
            ),

            # Heatmap
            html.Div([
                dcc.Graph(id='heatmap',
                          config={
                              "displaylogo": False,
                              "modeBarButtonsToRemove": ['zoom2d']
                          },
                          ),
                dcc.RadioItems(
                    id='map_chooser',
                    options=[
                        {'label': 'Heatmap', 'value': 'heatmap'},
                        {'label': 'Contour', 'value': 'contour'},
                        {'label': 'Surface', 'value': 'surface'}
                    ],
                    value='heatmap',
                    className='seven columns',
                    labelStyle={'display': 'inline-block'}
                )
            ],
                className='seven columns'
            ),
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

        @live_app.callback(
            [
                Output('log', 'children'),
                Output('log-entry', 'value'),
                Output('project-password', 'placeholder'),
                Output('project-password', 'value')
            ],
            [
                Input('submit-log-entry', 'n_clicks'),
            ],
            [
                State('log-entry', 'value'),
                State('project-password', 'value')
            ]
        )
        def update_output(n_clicks, log_entry, password):
            if n_clicks > 0:
                global encrypted_project_password
                global log
                encrypted_password = hashlib.sha256(password.encode()).hexdigest()

                if log_entry is "":
                    return [dcc.Markdown(log), "", "Enter project password...", ""]

                if encrypted_password != encrypted_project_password:
                    return [dcc.Markdown(log), log_entry, "Incorrect password...", ""]

                log += '\n --- \n **' + datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y") + '** \n\n' + log_entry
                return [dcc.Markdown(log), "", "Enter project password", ""]
