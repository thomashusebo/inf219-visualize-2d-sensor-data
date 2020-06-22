import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Output, Input

from webapp.figures import heatmap, linechart
from webapp.colors import ColorHandler
from webapp.apps.AbstractApp import AbstractApp
from webapp.terminateserver import shutdown_path, shutdown

#stylesheet = None
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
        ])

        @temporal_app.callback(Output("hidden_div", "children"),
                               [Input('url', 'pathname')])
        def shutdown_server(pathname):
            if pathname == shutdown_path:
                shutdown()
                return dcc.Location(pathname="/", id="someid_doesnt_matter")

        @temporal_app.callback(
            [
                Output(component_id='heatmap', component_property='figure'),
                Output(component_id='linechart', component_property='figure'),
                Output(component_id='live-clock', component_property='children'),
                Output(component_id='heatmap-slider', component_property='max')
            ],
            [
                Input('heatmap-slider', component_property='value'),
                Input('heatmap', component_property='clickData'),
                Input('interval-component', 'n_intervals'),
                Input('play-button', 'on'),

            ])
        def updateFigures(selectedIteration, clickData, n, playModeOn):
            # Collect data

            #data = data_manager.get_data()
            data=[]
            numberOfFrames = len(data)

            # Ensures that we avoid index out of bounds exceptions when accessing data
            if selectedIteration > numberOfFrames-1:
                selectedIteration = -1

            # Find slider position/iteration to display in heatmap
            if playModeOn:
                nextIteration = numberOfFrames-1
            else:
                nextIteration = selectedIteration-1

            # Define coordinate
            if clickData is not None:
                clickData = clickData['points'][0]
                coordinate = {'x': clickData['x'] - 1,
                              'y': clickData['y'] - 1}
            else:
                coordinate = {'x': 0, 'y': 0}

            # Define colormap
            colorScale = ColorHandler.getColorScale()

            # Update figures
            heatmapFig = heatmap.getHeatMap(data, nextIteration, colorScale)
            lineChartFig = linechart.getLineChart(data, nextIteration, coordinate, colorScale)

            return [
                heatmapFig,
                lineChartFig,
                "",
                #html.Span(datetime.datetime.now().strftime("%H:%M:%S")),
                numberOfFrames-1,
                ]
