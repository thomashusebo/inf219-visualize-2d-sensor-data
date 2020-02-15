import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

###########################################
## Setup a line chart data
x = [i for i in range(30)]
y = [(-1)**i*i**2 for i in x]


# Create line chart figure used in app from data and layout
linechart_data = go.Scatter(x=x,
                            y=y,
                            name="Close",
                            line=dict(color="#707eff")
                            )
linechart_layout = go.Layout(title=go.layout.Title(text="Line chart"))
linechart_fig = {
    'data':[linechart_data],
    'layout':linechart_layout
}
###########################################


app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
    # Title
    html.Div([
        html.H1("INF219 Visualization of 2d sensor data")
        ],
    ),

    # Heatmap
    html.Div([
        dcc.Graph(id='heatmap',
                  figure=heatmap_fig
                  )
        ],
        className='seven columns'
    ),

    # Line chart
    html.Div([
        dcc.Graph(id='linechart',
                  figure=linechart_fig)
        ],
        className='four columns'
    )
])

if __name__ =='__main__':
    app.run_server(debug=True)