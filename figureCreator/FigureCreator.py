from colorHandler import ColorHandler
import plotly.graph_objects as go


def getHeatMap(xs, ys, zs, color_scale):
    heatmap_data = go.Heatmap(x=xs,
                              y=ys,
                              z=zs,
                              colorscale=color_scale
                              )
    heatmap_layout = go.Layout(title=go.layout.Title(text='Heatmap Title'))

    heatmap_fig = {
        'data': [heatmap_data],
        'layout': heatmap_layout}

    return heatmap_fig, color_scale


def getLineChart(color_scale):
    x = [i for i in range(30)]
    y = [(-1) ** i * i ** 2 + i ** 2 + (i / 2) ** 2 for i in x]

    # Create line chart figure used in app from data and layout
    linechart_data = go.Scatter(x=x,
                                y=y,
                                name="Close",
                                line=dict(color=color_scale[0][1])
                                )
    linechart_layout = go.Layout(title=go.layout.Title(text="Line chart"))
    linechart_fig = {
        'data': [linechart_data],
        'layout': linechart_layout
    }
    return linechart_fig