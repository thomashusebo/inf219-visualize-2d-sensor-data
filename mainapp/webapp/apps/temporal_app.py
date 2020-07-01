import datetime
import time

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Output, Input, State

from mainapp.webapp.figures import heatmap, linechart
from mainapp.webapp.colors import color_manager
from mainapp.webapp.apps.abstract_app import AbstractApp
from mainapp.termination.termination import shutdown_path, shutdown_server

# stylesheet = None
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def check_for_coordinate(coordinates, coordinate):
    for point in coordinates:
        if point['x'] == coordinate['x'] and point['y'] == coordinate['y']:
            return True
    return False


class TemporalApp(AbstractApp):
    def setupOn(self, server, data_manager, project_name):
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
                   ## Project name: {}
                   '''.format(project_name))
            ],
            ),

            # Time
            html.Div([
                html.Div(id='live-clock'),
                dcc.Interval(
                    id='time-updater',
                    interval = 1*1000,
                    n_intervals=0
                ),
                dcc.Interval(
                    id='update_figure_interval',
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
                className='five columns'
            ),

            # Line chart
            html.Div([
                dcc.Graph(id='linechart',
                          config={
                              "displaylogo": False,
                              "modeBarButtonsToRemove": []
                          }),
            ],
                className='six columns'
            ),

            # Slider
            html.Div([
                daq.BooleanSwitch(
                    id='live-mode-button',
                    label="Update map to always show latest measurement: ",
                    labelPosition="top",
                    on=True
                ),
            ],
                className='three columns'
            ),
            dcc.RadioItems(
                id='map_chooser',
                options=[
                    {'label': 'Heatmap', 'value': 'heatmap'},
                    {'label': 'Contour', 'value': 'contour'},
                    {'label': 'Surface', 'value': 'surface'}
                ],
                value='contour',
                className='seven columns',
                labelStyle={'display': 'inline-block'}
            )
        ])

        @temporal_app.callback(Output("hidden_div", "children"),
                               [Input('url', 'pathname')])
        def shutdown(pathname):
            if pathname == shutdown_path:
                shutdown_server()
                return dcc.Location(pathname="/", id="someid_doesnt_matter")

        @temporal_app.callback(Output(component_id='live-clock', component_property='children'),
                               [Input('time-updater', 'n_intervals')])
        def update_clock(n):
            return html.Span(datetime.datetime.now().strftime("%H:%M:%S")),

        @temporal_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='linechart', component_property='figure'),
            ],
            [
                Input('update_figure_interval', 'n_intervals'),
                Input('heatmap', component_property='selectedData'),
                Input('heatmap', component_property='clickData'),
                Input('linechart', component_property='clickData'),
                Input('live-mode-button', 'on'),
                Input('map_chooser', 'value'),
            ],
            [
                State('linechart', 'relayoutData'),
            ])
        def updateFigures(n, selected_cells_heatmap, clicked_cell_heatmap, click_data_linechart, live_mode, map_type, relayout_data):
            timing = {}

            # Define default values
            first_tic = tic = time.process_time()
            default_timestamp = "2020-03-08 18:00:00"
            default_timeline = {'start': "2020-03-08 18:00:00", 'end': "2020-03-08 18:01:00"}
            default_coordinate = {'x': 0, 'y': 0}
            colorScale = color_manager.getColorScale()
            toc = time.process_time()
            timing['set default values'] = toc-tic

            # Choose coordinate
            tic = time.process_time()
            coordinates = [default_coordinate]
            if clicked_cell_heatmap is not None:
                coordinate = clicked_cell_heatmap['points'][0]
                coordinates = [coordinate]

            if selected_cells_heatmap is not None:
                if len(selected_cells_heatmap['points']) > 0:
                    coordinates = selected_cells_heatmap['points']
            toc = time.process_time()
            timing['choose coordinates'] = toc-tic

            # Check for timestamp data from linechart
            tic = time.process_time()
            timestamp = default_timestamp
            if click_data_linechart:
                timestamp = click_data_linechart['points'][0]['x']
            toc = time.process_time()
            timing['evaluate timestamp'] = toc-tic
            # Collect map data
            tic = time.process_time()
            latest_timestamp, heatmap_data = data_manager.get_heatmap_data(data_manager, timestamp=timestamp, live=live_mode)
            toc = time.process_time()
            timing['collect map data'] = toc-tic

            # Check current timeline in linechart and keep zoom level
            tic = time.process_time()
            timeline = default_timeline
            if live_mode and latest_timestamp is not None:
                latest_timestamp = datetime.datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S")
                timeline = {'start': latest_timestamp - datetime.timedelta(minutes=1), 'end':latest_timestamp+datetime.timedelta(seconds=2)}
                timestamp = latest_timestamp
            if relayout_data:
                if 'xaxis.range[0]' in relayout_data:
                    timeline = {'start': relayout_data['xaxis.range[0]'], 'end': relayout_data['xaxis.range[1]']}
            toc = time.process_time()
            timing['final say in timestamp and timeline'] = toc-tic

            # Collect linechart data
            tic = time.process_time()
            linechart_data = data_manager.get_linechart_data(data_manager, coordinates=coordinates, timeline=timeline)
            timing['collect line data'] =  time.process_time() - tic

            # Update figures
            tic = time.process_time()
            heatmapFig = heatmap.getHeatMap(heatmap_data, timestamp, colorScale, map_type, coordinates)
            toc = time.process_time()
            timing['update map fig'] = toc-tic

            tic = time.process_time()
            lineChartFig = linechart.getLineChart(linechart_data, timestamp, coordinates, colorScale, timeline)
            toc= time.process_time()
            timing['update line fig'] = toc-tic
            timing['full time'] = toc - first_tic
            print("Linechart figure update: {}".format(str(timing)))
            return [
                heatmapFig,
                lineChartFig,
            ]
