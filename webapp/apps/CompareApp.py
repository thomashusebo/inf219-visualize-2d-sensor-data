import dash
import dash_html_components as html
import dash_core_components as dcc
from webapp.apps.AbstractApp import AbstractApp
from webapp.terminateserver import shutdown_path, shutdown


class CompareApp(AbstractApp):
    def setupOn(self, server, data_manager):
        compare_app = dash.Dash(__name__, server=server, url_base_pathname=self.url)
        compare_app.layout = html.Div([
            html.H1('Compare View'),
            dcc.Location(id='url', refresh=False),
            html.Div(id="hidden_div"),
            dcc.Link('Shutdown server', href=shutdown_path),
        ])

        @compare_app.callback(dash.dependencies.Output("hidden_div", "children"),
                        [dash.dependencies.Input('url', 'pathname')])
        def shutdown_server(pathname):
            if pathname == shutdown_path:
                shutdown()
                return dcc.Location(pathname="/", id="someid_doesnt_matter")