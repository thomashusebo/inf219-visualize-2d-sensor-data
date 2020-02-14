import dash
import dash_html_components as html

app = dash.Dash()
app.layout = html.H1("INF219 Visualization of 2d sensor data")

if __name__ =='__main__':
    app.run_server(debug=True)