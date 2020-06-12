import dash
import dash_html_components as html
from flask import Flask
import webbrowser as wb

# Source: https://stackoverflow.com/questions/57685505/how-to-create-multiple-dashoards-using-plotly-dash-in-single-flask-app

def startServer():
    server = Flask(__name__)

    # Set-up endpoint 1
    app_1 = dash.Dash(__name__, server=server, url_base_pathname='/app1/')
    app_1.layout = html.H1('App 1')

    # Set-up endpoint 2
    app_2 = dash.Dash(__name__, server=server, url_base_pathname='/app2/')
    app_2.layout = html.H1('App 2')

    # Open URLs
    wb.open('http://127.0.0.1:5000/app1')
    wb.open('http://127.0.0.1:5000/app2')

    # Run server
    server.run()

