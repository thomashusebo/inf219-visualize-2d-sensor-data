import plotly.graph_objects as go


def getHeatMap(data, iterationID, colorScale):
    if len(data)==0: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

    oneFrame = data[iterationID]
    xs = oneFrame['xs']
    ys = oneFrame['ys']
    zs = oneFrame['zs']

    heatmap_data = go.Heatmap(x=xs,
                              y=ys,
                              z=zs,
                              colorscale=colorScale
                              )
    # heatmap_layout = go.Layout(title=go.layout.Title(text='Resistivity heatmap'))
    heatmap_layout = {
        'title': "Resistivity heatmap, {:d}/{:d}".format(iterationID + 1, len(data)),
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
