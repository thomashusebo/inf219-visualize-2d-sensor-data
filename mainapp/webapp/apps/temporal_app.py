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
                className='seven columns'
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
                Output(component_id='heatmap-slider', component_property='max')],
            [
                Input('heatmap-slider', component_property='value'),
                Input('heatmap', component_property='clickData'),
                Input('interval-component', 'n_intervals'),
                Input('play-button', 'on'),
                Input('map_chooser', 'value')],
            [
                State('linechart', 'relayoutData')])
        def updateFigures(selectedIteration, clickData, n, playModeOn, map_type, relayout_data):
            # Stops autoUpdate
            if not playModeOn:
                raise Exception("Preventing callback to update figures")

            # Define coordinate
            if clickData is not None:
                clickData = clickData['points'][0]
                coordinate = {'x': clickData['x'],
                              'y': clickData['y']}
            else:
                coordinate = {'x': 0, 'y': 0}

            # Define colormap
            colorScale = color_manager.getColorScale()

            # Collect data
            timestamp = "2020-03-08 18:00:00"
            timeline_start = "2020-03-08 18:00:00"
            timeline_end = "2020-03-08 21:00:00"

            if relayout_data:
                if 'xaxis.range[0]' in relayout_data:
                    timeline_start = relayout_data['xaxis.range[0]']
                    timeline_end = relayout_data['xaxis.range[1]']

            timeline = {'start': timeline_start, 'end': timeline_end}

            latest_timestamp, heatmap_data = data_manager.get_heatmap_data(data_manager, timestamp=timestamp)
            linechart_data = data_manager.get_linechart_data(data_manager, coordinate=coordinate, timeline=timeline)

            # Update figures
            heatmapFig = heatmap.getHeatMap(heatmap_data, timestamp, colorScale, map_type)
            lineChartFig = linechart.getLineChart(linechart_data, timestamp, coordinate, colorScale, timeline)

            return [
                heatmapFig,
                lineChartFig,
                html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
                1,
            ]
