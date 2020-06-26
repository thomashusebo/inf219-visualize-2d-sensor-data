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

    heatmap_data = get_figure[figure_type](z=data,
                              colorscale=colorScale
                              )

    heatmap_layout = {
        'title': "Resistivity heatmap: {}".format(timestamp),
        'yaxis': {
            "scaleanchor": "x",
            "scaleratio": 1,
        },
        'margin': {
            'l': 40,
            'r': 40,
            't': 40,
            'b': 25
        },
        'colorbar': {
            "title": "Resistivity (Ohm)"
        }
    }

    heatmap_fig = {
        'data': [heatmap_data],
        'layout': heatmap_layout
    }

    return heatmap_fig
