import dash
import dash_html_components as html
import dash_core_components as dcc
from flask import Flask, request
import webbrowser as wb

# Inspiration:
#  - https://stackoverflow.com/questions/57685505/how-to-create-multiple-dashoards-using-plotly-dash-in-single-flask-app
#  - https://stackoverflow.com/questions/55620642/plotly-dash-python-how-to-stop-execution-after-time
shutdown_path = '/shutdown'


def startServer():
    server = Flask(__name__)

    # Set-up endpoint 1
    app_1 = dash.Dash(__name__, server=server, url_base_pathname='/app1/')
    app_1.layout = html.Div([
        html.H1('App 1'),
        dcc.Location(id='url', refresh=False),
        html.Div(id="hidden_div"),
        dcc.Link('Shutdown server', href=shutdown_path),
    ])

    @app_1.callback(dash.dependencies.Output("hidden_div", "children"),
                  [dash.dependencies.Input('url', 'pathname')])
    def shutdown_server(pathname):
        if pathname == shutdown_path:
            shutdown()
            return dcc.Location(pathname="/", id="someid_doesnt_matter")

    # Set-up endpoint 2
    app_2 = dash.Dash(__name__, server=server, url_base_pathname='/app2/')
    app_2.layout = html.Div([
        html.H1('App 2'),
        dcc.Location(id='url', refresh=False),
        html.Div(id="hidden_div"),
        dcc.Link('Shutdown server', href=shutdown_path),
    ])

    @app_2.callback(dash.dependencies.Output("hidden_div", "children"),
                  [dash.dependencies.Input('url', 'pathname')])
    def shutdown_server(pathname):
        if pathname == shutdown_path:
            shutdown()
            return dcc.Location(pathname="/", id="someid_doesnt_matter")

    # Open URLs
    wb.open('http://127.0.0.1:5000/app1')
    wb.open('http://127.0.0.1:5000/app2')

    # Run server
    server.run()


def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
