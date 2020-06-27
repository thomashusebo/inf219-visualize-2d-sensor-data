import plotly.graph_objects as go


def getHeatMap(data, timestamp, colorScale, figure_type):
    get_figure = {
        'heatmap': go.Heatmap,
        'contour': go.Contour,
        'surface': go.Surface
    }

    if len(data) == 0: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

    heatmap_fig = go.Figure(data=get_figure[figure_type](z=data,
                              colorscale=colorScale
                              ),
                            )
    heatmap_fig.update_layout(
        title="Resistivity heatmap: {}".format(timestamp),
        yaxis=dict(
            scaleanchor = "x",
            scaleratio=1
        ),
        margin=dict(
            l=40,
            r=40,
            t=40,
            b=25,
        ),
    )
    return heatmap_fig


