import base64
import datetime
import time

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
                'padding-left': '2%',
                'padding-right': '2%',
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
                                            'width': '55%',
                                            'height': 'auto',
                                        }
                                    ),
                                    className='four columns',
                                    style={
                                        'width': '{}%'.format(4 / 12 * 100 - 0.2),
                                        'padding-top': '0.5%',
                                        'border': 0,
                                        'margin': '0.1%',
                                        'background-color': 'white',
                                    },
                                ),
                                html.Div(
                                    className='four columns',
                                    style={
                                        'width': '{}%'.format(4 / 12 * 100 - 0.2),
                                        'padding-top': '2%',
                                        'padding-right': '0.5%',
                                        'border': 0,
                                        'margin': '0.1%',
                                        'text-align': 'right',
                                        'background-color': 'white'
                                    },
                                    children=[
                                        html.H1('Monitor'),
                                    ]
                                ),

                                html.Div(
                                    className='four columns',
                                    style={
                                        'width': '{}%'.format(4 / 12 * 100 - 0.2),
                                        'padding-top': '2%',
                                        'padding-right': '0.5%',
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
                    className='five columns',
                    style={**puzzlebox,
                           **{'width': '{}%'.format(5 / 12 * 100)}},
                    children=[
                        dcc.Markdown(
                            children='''##### Project: {}'''.format(project_name)
                        ),
                        html.Div(
                            id='log',
                            style={
                                'padding-left': '1%',
                                'padding-right': '-1%',
                                'margin-bottom': '1%',
                                'background-color': 'white',
                                'width': '100%',
                                'height': 400,
                                # Make area scrollable
                                'overflow-x': 'hidden',
                                'overflow-y': 'auto',
                                'text-align': 'left',
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
                html.Div([
                    html.Div(
                        className='six columns',
                        style={**puzzlebox,
                               **{'width': '{}%'.format(6 / 12 * 100)}},
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
                                className='six columns',
                                options=[
                                    {'label': 'Heatmap', 'value': 'heatmap'},
                                    {'label': 'Contour', 'value': 'contour'},
                                ],
                                value='heatmap',
                                labelStyle={'display': 'inline-block'}
                            ),
                        ],
                    ),
                    html.Div(
                        className='one columns',
                        style={**puzzlebox,
                               **{'min-width': None,
                                  'width': '{}%'.format(1/12*100-0.1*6)}},
                        children=[
                            dcc.Input(
                                id="color-high",
                                type='number',
                                placeholder='Max val',
                                style={
                                    'width': '100%',
                                    'margin-bottom': 100
                                },
                                value=12000,
                            ),
                            dcc.Input(
                                id="color-low",
                                type='number',
                                placeholder= 'Min val',
                                style={
                                    'width': '100%',
                                    'margin-top': 100
                                },
                                value=0,
                            ),
                        ]
                    ),
                ]),

                # Line chart
                html.Div(
                    className='seven columns',
                    style={**puzzlebox,
                           **{'width': '{}%'.format(7 / 12 * 100-0.1*4)}},
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
        def update_clock(_):
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
                Input('map_chooser', 'value'),
                Input('color-low', 'value'),
                Input('color-high', 'value'),
            ],
            [
                State('linechart', 'relayoutData'),
            ]
        )
        def updateFigures(_, selected_cells_heatmap, clicked_cell_heatmap, plot_type, col_min, col_max, linechart_data):
            tic = time.process_time()

            # Define colormap
            colorScale = color_manager.getColorScale()
            color_range = {'min': col_min, 'max': col_max}

            # Choose coordinate
            default_coordinate = {'x': 0, 'y': 0}
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

            timeline = {'start': last_timestamp - datetime.timedelta(minutes=60),
                        'end': last_timestamp + datetime.timedelta(seconds=0)}
            if linechart_data:
                if 'xaxis.range[0]' in linechart_data:
                    start = datetime.datetime.strptime(linechart_data['xaxis.range[0]'], "%Y-%m-%d %H:%M:%S")
                    end = datetime.datetime.strptime(linechart_data['xaxis.range[1]'], "%Y-%m-%dT%H:%M:%S")
                    timeline['start'] = last_timestamp - (end-start)
            linechart_data = data_manager.get_linechart_data(data_manager, coordinates=coordinates, timeline=timeline)

            # Update figures
            heatmapFig = heatmap.getHeatMap(heatmap_data, last_timestamp, colorScale, plot_type, coordinates, 'white',
                                            color_range)
            lineChartFig = linechart.getLineChart(linechart_data, last_timestamp, coordinates, colorScale, timeline, color_range)
            toc = time.process_time()
            print("Time to update figures(Live): {}".format(toc-tic))
            return [
                heatmapFig,
                lineChartFig
            ]

        @live_app.callback(
            [
                Output('log', 'children'),
                Output('log-entry', 'value'),
                Output('log-entry', 'placeholder'),
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
        def update_log(n_clicks, log_entry, password):
            global log
            log_entry_value = log_entry
            log_entry_placeholder = "Write log entry..."
            password_value = ""
            password_placeholder = "Enter password..."

            if n_clicks > 0:
                if log_entry is "" or log_entry is None:
                    log_entry_placeholder = "Cannot submit empty log entry..."
                else:
                    if password is not None:
                        if project_manager.verify_password(project_name, password):
                            timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                            log_manager.insert_log_entry(timestamp, log_entry)
                            log = log_manager.retrieve_log()
                            log_entry_value = ""
                        else:
                            password_placeholder = "Incorrect password...."
            return [
                dcc.Markdown(log),
                log_entry_value,
                log_entry_placeholder,
                password_placeholder,
                password_value
            ]
