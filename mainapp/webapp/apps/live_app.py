import datetime
import hashlib

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State

from mainapp.webapp.apps.abstract_app import AbstractApp
from mainapp.webapp.figures import heatmap
from mainapp.webapp.colors import color_manager

# stylesheet = None
from mainapp.webapp.log_manager import LogManager
from storage.project_manager import ProjectManager

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
log = ""
database_manager = ProjectManager()
log_manager = None


class LiveApp(AbstractApp):
    def setupOn(self, server, data_manager, project_name):
        global log_manager, log
        log_manager = LogManager(project_name)
        log = log_manager.retrieve_log()

        live_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        live_app.layout = html.Div([
            # Page Header
            html.Div([
                html.H1('Live View'),
                html.A('Shutdown Server', href='/settings'),

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
            global log

            if log_entry is "":
                return [dcc.Markdown(log), "", "Enter project password...", ""]

            if password is not None:
                if database_manager.verify_password(project_name, password):
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                    log_manager.insert_log_entry(timestamp, log_entry)
                    log = log_manager.retrieve_log()
                else:
                    return [dcc.Markdown(log), log_entry, "Incorrect password...", ""]

            return [dcc.Markdown(log), "", "Enter project password", ""]
