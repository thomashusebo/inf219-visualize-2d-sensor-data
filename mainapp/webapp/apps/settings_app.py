from dash import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State

from mainapp.termination.termination import shutdown_software
from mainapp.webapp.apps.abstract_app import AbstractApp
from storage.project_manager import ProjectManager

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class SettingsApp(AbstractApp):

    def setupOn(self, server, data_manager, project_name):
        settings_app = dash.Dash(__name__, server=server, url_base_pathname=self.url, external_stylesheets=stylesheet)
        settings_app.layout = html.Div(
            style={
                'padding-top': '10%'
            },
            children=[
                html.Div(
                    className='six columns offset-by-three',
                    style={
                        'background-color': '#edf5ff',
                        'padding-top': '3%',
                        'padding-bottom': '5%',
                        'padding-left': '5%',
                        'padding-right': '5%',
                    },
                    children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div([
                                    html.H3(
                                        style={
                                          'padding': '0%'
                                        },
                                        children='Do you want to shutdown the visualization tool?',
                                    ),
                                ])
                            ],
                        ),
                        html.Div(
                            className='row',
                            children=[
                                dcc.Input(
                                    id="project-password",
                                    type='password',
                                    placeholder="Enter project password...",
                                    value=""
                                ),
                                html.Button(
                                    children='Shutdown',
                                    id='shutdown',
                                    n_clicks=0,
                                    style={
                                        'background-color': 'red',
                                        'color': 'white'
                                    }
                                ),
                            ],
                        )
                    ],
                ),
            ]
        )

        @settings_app.callback([Output('project-password', 'value'),
                                Output('project-password', 'placeholder')
                                ],
                               [Input('shutdown', 'n_clicks')],
                               [State('project-password', 'value')])
        def stop_software(n_clicks, password):
            value="",
            placeholder = "Enter password...",
            if n_clicks > 0:
                if ProjectManager().verify_password(project_name, password):
                    shutdown_software()
                    placeholder = "Shutting down..."
                else:
                    placeholder= "Incorrect password..."
            return [value, placeholder]
