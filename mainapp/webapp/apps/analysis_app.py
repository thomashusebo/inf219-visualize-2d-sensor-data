import base64
import datetime
import time
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from pandas import DataFrame

from mainapp.app_settings import datetime_format
from mainapp.webapp import calibrator
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


def calibrate_map(heatmap_data, calibration_data):
    return np.subtract(heatmap_data, calibration_data)


def calibrate_line_data(linechart_data, calibration_data, coordinates):
    calibration = [""]
    for coord in coordinates:
        calibration.append(-calibration_data[coord['x'], coord['y']])

    return linechart_data+calibration


class AnalysisApp(AbstractApp):
    def setupOn(self, server, data_manager, project_name):
        global log_manager, log
        log_manager = LogManager(project_name)
        log = log_manager.retrieve_log()
        analysis_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        analysis_app.layout = html.Div(
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
                                        html.H1('Explore'),
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

                # Project name
                html.Div(
                    className='five columns',
                    style={**puzzlebox,
                           **{
                               'width': '{}%'.format(5 / 12 * 100),
                           }},
                    children=[
                        html.Div(
                            style={**puzzlebox,
                                   **{
                                       'width': '100%',
                                   }},
                            children=[
                                dcc.Markdown(
                                    children='''### Project: {}'''.format(project_name)
                                ),
                            ]
                        ),

                        # Calibration
                        html.Div(
                            style={**puzzlebox,
                                   **{
                                       'width': '100%',
                                       'height': 375
                                   }},
                            children=[
                                dcc.Markdown(
                                    '--- \n\n'
                                    '##### Add new Calibration'
                                ),
                                dcc.Markdown(
                                    'Selected timestamp: None',
                                    id='display-selected-timestamp',
                                ),
                                dcc.Input(
                                    id='calibration-name',
                                    maxLength=25,
                                    style={
                                        'width': '50%',
                                    },
                                    placeholder='Enter descriptive name...'
                                ),
                                dcc.Input(
                                    id="project-password",
                                    type='password',
                                    placeholder="Enter project password...",
                                    style={'width': '50%'}
                                ),
                                dcc.Store(id='selected-timestamp'),
                                html.Button('Add New Calibration', id='submit-new-calibration', n_clicks=0),
                            ],
                        ),
                        dcc.Dropdown(
                            id='calibration-dropdown',
                            options=[
                                {'label': 'None', 'value': None},
                            ],
                            value=None
                        )
                    ]
                ),


                # Heatmap
                html.Div([
                    html.Div(
                        className='six columns',
                        style={**puzzlebox,
                               **{'width': '{}%'.format(2 / 12 * 100 - 0.2),
                                  'min-width':None}},
                        children=[
                            dcc.Graph(
                                id='raw_map',
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
                                }
                            )
                        ]
                    ),
                    html.Div(
                        className='six columns',
                        style={**puzzlebox,
                               **{'width': '{}%'.format(2 / 12 * 100 - 0.2),
                                  'min-width':None}},
                        children=[
                        ]
                    ),
                    html.Div(
                        className='six columns',
                        style={**puzzlebox,
                               **{'width': '{}%'.format(2 / 12 * 100 - 0.2),
                                  'min-width':None}},
                        children=[
                            dcc.Graph(
                                id='calibration_map',
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
                                }
                            )
                        ]
                    ),
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
                                    'margin-bottom': 96
                                },
                                value=10000,
                            ),
                            dcc.Input(
                                id="color-low",
                                type='number',
                                placeholder='Min val',
                                style={
                                    'width': '100%',
                                    'margin-top': 96
                                },
                                value=-10000,
                            ),
                        ]
                    ),
                    html.Div(
                        className='one columns',
                        style={**puzzlebox,
                               **{
                                   'background-color': 'white',
                                   'min-width': None,
                                   'width': '{}%'.format(1 / 12 * 100 - 0.1 * 6)}},
                        children=[
                            html.Button(
                                'Refresh',
                                id='refresh',
                                style={
                                    'background-color': 'white',
                                    'padding': '0.5%',
                                    'margin': '0.1%',
                                    'color': 'blue',
                                    'width': '100%',
                                    'text-align': 'center',
                                }
                            )
                        ]
                    ),
                ]),

                # Line chart
                html.Div(
                    className='seven columns',
                    style={**puzzlebox,
                           **{'width': '{}%'.format(12 / 12 * 100-0.2)}},
                    children=[
                        dcc.Graph(
                            id='linechart',
                            config={
                                "displaylogo": False,
                                "modeBarButtonsToRemove": [
                                    'lasso2d',
                                    'select2d',
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

        @analysis_app.callback(
            [
                Output(component_id='calibration-name', component_property='placeholder'),
                Output(component_id='calibration-name', component_property='value'),
                Output(component_id='project-password', component_property='placeholder'),
                Output(component_id='project-password', component_property='value'),
                Output(component_id='calibration-dropdown', component_property='options')
            ],
            [
                Input(component_id='submit-new-calibration', component_property='n_clicks')
            ],

            [
                State(component_id='selected-timestamp', component_property='data'),
                State(component_id='calibration-name', component_property='value'),
                State(component_id='project-password', component_property='value')
            ]
        )
        def add_calibration(n_clicks, timestamp, calibration_name, password):
            name_value = calibration_name
            name_placeholder = "Enter descriptive name..."
            password_value = ""
            password_placeholder = "Enter project password..."
            options = [{'label': 'None', 'value': None}]

            if timestamp is None and n_clicks > 0:
                password_placeholder = "Must choose a timestamp from linechart"
            else:
                if password is not None:
                    if project_manager.verify_password(project_name, password):
                        calibrator.add_calibration(project_name, calibration_name, timestamp)
                        name_value = ""
                    else:
                        password_placeholder = "Incorrect password..."

            calibrations = calibrator.get_all_calibration_times(project_name)
            if calibrations is not None:
                for _, row in calibrations.iterrows():
                    options.append({'label': row['calibrationname'], 'value': row['time']})

            return [
                name_placeholder,
                name_value,
                password_placeholder,
                password_value,
                options
            ]

        @analysis_app.callback(
            [Output(component_id='live-clock', component_property='children')],
            [Input(component_id='interval-component', component_property='n_intervals')]
        )
        def update_clock(_):
            return dcc.Markdown(datetime.datetime.now().strftime("%H:%M:%S")),

        @analysis_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='linechart', component_property='figure'),
                Output(component_id='display-selected-timestamp', component_property='children'),
                Output(component_id='selected-timestamp', component_property='data'),
                Output(component_id='raw_map', component_property='figure'),
                Output(component_id='calibration_map', component_property='figure'),
            ],
            [
                Input('heatmap', 'selectedData'),
                Input('heatmap', 'clickData'),
                Input('linechart', 'clickData'),
                Input('map_chooser', 'value'),
                Input('color-low', 'value'),
                Input('color-high', 'value'),
                Input('refresh', 'n_clicks'),
                Input('calibration-dropdown', 'value')
            ],
            [
                State('linechart', 'relayoutData'),
            ]
        )
        def updateFigures(
                selected_cells_heatmap,
                clicked_cell_heatmap,
                linechart_click_data,
                plot_type,
                col_min,
                col_max,
                _,
                calibration_time,
                linechart_data):
            tic = time.process_time()

            # Define colormap
            colorScale = color_manager.getColorScale('red-white-blue')
            color_range = {'min': col_min, 'max': col_max}
            meta_color_scale = color_manager.getColorScale('green-yellow')
            meta_color_range = {'min': 0, 'max': 12000}

            # Choose coordinate
            default_coordinate = {'x': 0, 'y': 0}
            coordinates = [default_coordinate]
            if clicked_cell_heatmap is not None:
                coordinate = clicked_cell_heatmap['points'][0]
                coordinates = [coordinate]
            if selected_cells_heatmap is not None:
                if len(selected_cells_heatmap['points']) > 0:
                    coordinates = selected_cells_heatmap['points']

            # Check for timestamp
            timestamp = project_manager.get_last_timestamp(project_name)
            selected_timestamp = None
            if linechart_click_data:
                timestamp = selected_timestamp = linechart_click_data['points'][0]['x']

            if timestamp is None:
                raise PreventUpdate("No timestamp found")
            timestamp = datetime.datetime.strptime(timestamp, datetime_format)


            # Collect data
            last_timestamp, heatmap_data = data_manager.get_heatmap_data(data_manager, timestamp=timestamp, live=False)
            last_timestamp = datetime.datetime.strptime(last_timestamp, datetime_format)

            timeline = {'start': timestamp - datetime.timedelta(minutes=60),
                        'end': timestamp + datetime.timedelta(minutes=2)}
            if linechart_data:
                if 'xaxis.range[0]' in linechart_data:
                    timeline = {'start': linechart_data['xaxis.range[0]'], 'end': linechart_data['xaxis.range[1]']}

            linechart_data = data_manager.get_linechart_data(
                data_manager,
                coordinates=coordinates,
                timeline=timeline,
                get_all=True)

            # Calibrate
            calibrated_data = heatmap_data
            calibration_data = DataFrame()
            if calibration_time is not None:
                calibration_data = calibrator.get_map_calibration_data(project_name, calibration_time)
                calibrated_data = calibrate_map(heatmap_data, calibration_data)
                linechart_data = calibrate_line_data(linechart_data, calibration_data, coordinates)

            # Update figures
            raw_fig = heatmap.getHeatMap(
                heatmap_data,
                timestamp,
                meta_color_scale,
                plot_type,
                coordinates,
                'white',
                meta_color_range,
                figure_height=150,
                title='Raw data',
                axis_name=False
            )
            calibrated_fig = heatmap.getHeatMap(
                calibrated_data,
                timestamp,
                colorScale,
                plot_type,
                coordinates,
                'white',
                color_range,
            )
            calibration_fig = heatmap.getHeatMap(
                data=calibration_data,
                timestamp=calibration_time,
                colorScale=meta_color_scale,
                figure_type=plot_type,
                coordinates=coordinates,
                background_color='white',
                custom_color_range=meta_color_range,
                figure_height=150,
                title='Calibration data',
                axis_name=False
            )
            lineChartFig = linechart.getLineChart(
                linechart_data,
                timestamp,
                coordinates,
                colorScale,
                timeline,
                color_range,
                dragmode='pan',
                quick_select_range=False,
                calibration_time=calibration_time,
            )
            toc = time.process_time()
            print("Time to update figures (Analysis): {}".format(toc-tic))
            return [
                calibrated_fig,
                lineChartFig,
                'Selected timestamp: {}'.format(selected_timestamp),
                selected_timestamp,
                raw_fig,
                calibration_fig
            ]
