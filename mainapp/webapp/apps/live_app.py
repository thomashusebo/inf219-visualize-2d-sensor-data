import base64
import datetime
import hashlib

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State

from mainapp.webapp.apps.abstract_app import AbstractApp
from mainapp.webapp.figures import heatmap, linechart
from mainapp.webapp.colors import color_manager

# stylesheet = None
from mainapp.webapp.log_manager import LogManager
from storage.project_manager import ProjectManager

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
log = ""
project_manager = ProjectManager()
log_manager = None
logo = 'assets/fluidflower-logo.png'
encoded_logo = base64.b64encode(open(logo, 'rb').read()).decode('ascii')
background_color = '#f0f0f0'
puzzlebox = {
    'background-color': background_color,
    'padding': '0.5%',
    'border': 0,
    'margin': '0.1%',
    'min-width': 400,
}


class LiveApp(AbstractApp):
    def setupOn(self, server, data_manager, project_name):
        global log_manager, log
        log_manager = LogManager(project_name)
        log = log_manager.retrieve_log()

        live_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        live_app.layout = html.Div(
            style={
                'padding-left': '10%',
                'padding-right': '10%',
            },
            children=[
                # Page Header
                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    html.Img(
                                        src='data:image/png;base64,{}'.format(encoded_logo),
                                        style={
                                            'width': '40%',
                                            'height': 'auto',
                                        }
                                    ),
                                    className='six columns',
                                    style={
                                        'padding-top': '2%',
                                        'border': 0,
                                        'margin': '0.1%',
                                        'background-color': 'white'
                                    },
                                ),
                                html.Div(
                                    className='six columns',
                                    style={
                                        'padding-top': '2%',
                                        'padding-right': '2%',
                                        'border': 0,
                                        'margin': '0.1%',
                                        'text-align': 'right',
                                        'background-color': 'white'
                                    },
                                    children=[
                                        dcc.Link(html.Button('Settings'), href='/settings', refresh=True),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),

                # Log
                html.Div(
                    className='six columns',
                    style=puzzlebox,
                    children=[
                        # '''dcc.Markdown(
                        #    children='''##### Log'''),'''
                        html.Div(
                            id='log',
                            style={
                                'padding-left': '1%',
                                'padding-right': '-1%',
                                'margin-bottom': '1%',
                                'background-color': 'white',
                                'width': '100%',
                                'height': 450,
                                # Make area scrollable
                                'overflow-x': 'hidden',
                                'overflow-y': 'auto',
                                'text-align': 'justify',
                                # Keep scroll at bottom:
                                'display': 'flex',
                                'flex-direction': 'column-reverse',
                            },
                            children=dcc.Markdown(log)),
                        dcc.Textarea(
                            id='log-entry',
                            style={'width': '100%', 'height': 87},
                            placeholder='Enter log entry...'
                        ),
                        dcc.Input(
                            id="project-password",
                            type='password',
                            placeholder="Enter project password...",
                            style={'width': '50%'}
                        ),
                        html.Button('Submit', id='submit-log-entry', n_clicks=0),
                    ],
                ),

                # Heatmap
                html.Div(
                    className='six columns',
                    style=puzzlebox,
                    children=[
                        dcc.Graph(
                            id='heatmap',
                            config={
                                "displaylogo": False,
                                "modeBarButtonsToRemove": [
                                    'zoom2d',
                                    'pan2d',
                                    'select2d',
                                    'zoomIn2d',
                                    'zoomOut2d',
                                    'autoScale2d',
                                    'resetScale2d',
                                    'toggleSpikelines',
                                ]
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
                            labelStyle={'display': 'inline-block'}
                        ),
                    ],
                ),

                # Line chart
                html.Div(
                    className='six columns',
                    style=puzzlebox,
                    children=[
                        dcc.Graph(
                            id='linechart',
                            config={
                                "displaylogo": False,
                                "modeBarButtonsToRemove": [
                                    'zoom2d',
                                    'pan2d',
                                    'lasso2d',
                                    'select2d',
                                    'zoomIn2d',
                                    'zoomOut2d',
                                    'autoScale2d',
                                    'toggleSpikelines',
                                ]
                            }
                        ),
                    ],
                ),
                html.Div(
                    className='six columns',
                    style={**puzzlebox,
                           **{'background-color': 'white'}},
                    children=html.Span(""),
                ),
                html.Div(
                    className='six columns',
                    style={
                        'padding-top': '0.1%',
                        'padding-right': '2%',
                        'border': 0,
                        'margin': '0.1%',
                        'text-align': 'right',
                        'background-color': 'white'
                    },
                    children=[
                        html.Div(id='live-clock'),
                        dcc.Interval(
                            id='interval-component',
                            interval=1 * 1000,  # milliseconds
                            n_intervals=0
                        ),
                    ]
                )
            ]
        )

        @live_app.callback(
            [Output(component_id='live-clock', component_property='children')],
            [Input(component_id='interval-component', component_property='n_intervals')]
        )
        def update_clock(n):
            return dcc.Markdown(datetime.datetime.now().strftime("%H:%M:%S")),

        @live_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='linechart', component_property='figure')
            ],
            [
                Input('interval-component', 'n_intervals'),
                Input('heatmap', 'selectedData'),
                Input('heatmap', 'clickData'),
                Input('map_chooser', 'value')
            ])
        def updateFigures(nIntervals, selected_cells_heatmap, clicked_cell_heatmap, plot_type):

            # Define colormap
            colorScale = color_manager.getColorScale()
            default_coordinate = {'x': 0, 'y': 0}

            # Choose coordinate
            coordinates = [default_coordinate]
            if clicked_cell_heatmap is not None:
                coordinate = clicked_cell_heatmap['points'][0]
                coordinates = [coordinate]
            if selected_cells_heatmap is not None:
                if len(selected_cells_heatmap['points']) > 0:
                    coordinates = selected_cells_heatmap['points']

            # Collect data
            last_timestamp, heatmap_data = data_manager.get_heatmap_data(data_manager, live=True)
            last_timestamp = datetime.datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")

            timeline = {'start': last_timestamp - datetime.timedelta(minutes=1),
                        'end': last_timestamp + datetime.timedelta(seconds=2)}
            linechart_data = data_manager.get_linechart_data(data_manager, coordinates=coordinates, timeline=timeline)

            # Update figures
            heatmapFig = heatmap.getHeatMap(heatmap_data, last_timestamp, colorScale, plot_type, coordinates, background_color)
            lineChartFig = linechart.getLineChart(linechart_data, last_timestamp, coordinates, colorScale, timeline)
            return [
                heatmapFig,
                lineChartFig
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
                if project_manager.verify_password(project_name, password):
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                    log_manager.insert_log_entry(timestamp, log_entry)
                    log = log_manager.retrieve_log()
                else:
                    return [dcc.Markdown(log), log_entry, "Incorrect password...", ""]

            return [dcc.Markdown(log), "", "Enter project password", ""]
