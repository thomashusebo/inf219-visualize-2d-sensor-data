import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html


def setup(app):
    app.layout = html.Div([
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
            className='three columns'
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

    return None
