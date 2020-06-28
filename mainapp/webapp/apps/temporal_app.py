import datetime

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
    def setupOn(self, server, data_manager):
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
                   ## Project name:
                   ''')
            ],
            ),

            # Time
            html.Div([
                html.Div(id='live-clock'),
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

        @temporal_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='linechart', component_property='figure'),
                Output(component_id='live-clock', component_property='children'),
            ],
            [
                Input('update_figure_interval', component_property='n_intervals'),
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
            # Define default values
            default_timestamp = "2020-03-08 18:00:00"
            default_timeline = {'start': "2020-03-08 18:00:00", 'end': "2020-03-08 18:01:00"}
            default_coordinate = {'x': 0, 'y': 0}
            colorScale = color_manager.getColorScale()

            # Choose coordinate
            coordinates = [default_coordinate]
            if clicked_cell_heatmap is not None:
                coordinate = clicked_cell_heatmap['points'][0]
                coordinates = [coordinate]

            if selected_cells_heatmap is not None:
                if len(selected_cells_heatmap['points']) > 0:
                    coordinates = selected_cells_heatmap['points']

            # Check for timestamp data from linechart
            timestamp = default_timestamp
            if click_data_linechart:
                timestamp = click_data_linechart['points'][0]['x']

            # Collect map data
            latest_timestamp, heatmap_data = data_manager.get_heatmap_data(data_manager, timestamp=timestamp, live=live_mode)

            # Check current timeline in linechart and keep zoom level
            timeline = default_timeline
            if live_mode:
                latest_timestamp = datetime.datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S")
                timeline = {'start': latest_timestamp - datetime.timedelta(minutes=1), 'end':latest_timestamp+datetime.timedelta(seconds=2)}
            if relayout_data:
                if 'xaxis.range[0]' in relayout_data:
                    timeline = {'start': relayout_data['xaxis.range[0]'], 'end': relayout_data['xaxis.range[1]']}

            # Collect linechart data
            linechart_data = data_manager.get_linechart_data(data_manager, coordinates=coordinates, timeline=timeline)

            if live_mode:
                timestamp = latest_timestamp

            # Update figures
            heatmapFig = heatmap.getHeatMap(heatmap_data, timestamp, colorScale, map_type, coordinates)
            lineChartFig = linechart.getLineChart(linechart_data, timestamp, coordinates, colorScale, timeline)

            return [
                heatmapFig,
                lineChartFig,
                html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
            ]
