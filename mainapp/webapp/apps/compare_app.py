import dash
import dash_html_components as html
import dash_core_components as dcc
from mainapp.webapp.apps.abstract_app import AbstractApp
from mainapp.termination.termination import shutdown_path, shutdown_software

#stylesheet = None
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class CompareApp(AbstractApp):
    def setupOn(self, server, data_manager, project_name):
        compare_app = dash.Dash(__name__, server=server, url_base_pathname=self.url)
        compare_app.layout = html.Div([
            html.H1('Compare View'),
            html.A('Shutdown Server', href='/settings'),
    ])