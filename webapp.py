import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go

####################################################
## Setup a heatmap data
n = 14                                  # number of columns
m = 7                                   # number of rows
xs = [i for i in range(1,n+1)]          # Defines x's
ys = [i for i in range(1, m+1)]         # Defines y's
zs = [[i * j for i in xs] for j in ys]  # Defines plotted value in heatmap

# Create heatmap figure used in app from data and layout
heatmap_data = go.Heatmap(x=xs,
                          y=ys,
                          z=zs,
                          )
heatmap_layout = go.Layout(title=go.layout.Title(text='Heatmap Title'))

heatmap_fig = {
    'data':[heatmap_data],
    'layout':heatmap_layout}
###################################################

app = dash.Dash()
app.layout = html.Div([
    # Title
    html.Div(html.H1("INF219 Visualization of 2d sensor data")),

    # Heatmap
    html.Div([
        dcc.Graph(id='heatmap',
                  figure=heatmap_fig
                  )
    ])
])

if __name__ =='__main__':
    app.run_server(debug=True)