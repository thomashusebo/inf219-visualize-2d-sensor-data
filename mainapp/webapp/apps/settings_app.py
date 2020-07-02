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
        settings_app.layout = html.Div([
            html.Div([
                html.Div(id='hidden_div'),
                html.H3('Do you want to shutdown the visualization tool?'),
                dcc.Input(
                    id="project-password",
                    type='password',
                    placeholder="Enter project password...",
                    value=""
                ),
                html.Button('Shutdown', id='shutdown', n_clicks=0),
            ])
        ])

        @settings_app.callback([Output('hidden_div', 'children'),
                                Output('project-password', 'value'),
                                Output('project-password', 'placeholder')
                                ],
                               [Input('shutdown', 'n_clicks')],
                               [State('project-password', 'value')])
        def stop_software(n_clicks, password):
            if n_clicks > 0:
                if ProjectManager().verify_password(project_name, password):
                    shutdown_software()
                    return [dcc.Location(pathname="/", id="someid_doesnt_matter"), "", "Shutting down..."]
                else:
                    return [None, "", "Incorrect password..."]

