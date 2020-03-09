import datetime

import plotly.graph_objects as go


def getHeatMap(data, iterationID, colorScale):
    if iterationID < 0: return {
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
        'title': "Resistivity heatmap, measurement {:d}/{:d}".format(iterationID + 1, len(data)),
        'yaxis': {
            "scaleanchor": "x",
            "scaleratio": 1,
        },
        'margin': {
            'l': 40,
            'r': 40,
            't': 40,
            'b': 25
        }
    }

    heatmap_fig = {
        'data': [heatmap_data],
        'layout': heatmap_layout
    }

    return heatmap_fig


def getLineChart(data, iterationID, coordinate, colorScale):
    if iterationID < 0: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

    minValue = min(min(data[iterationID]['zs']))
    maxValue = max(max(data[iterationID]['zs']))

    x = coordinate['x']
    y = coordinate['y']
    ts = [i for i in range(len(data))]
    zs = [data[i]['zs'][y][x] for i in range(len(data))]

    keepTrackOfIteration = go.Scatter(x=[iterationID, iterationID],
                                      y=[0, zs[iterationID]],
                                      name="Timestep",
                                      line=dict(color=colorScale[10][1]),
                                      )

    linechart_data = go.Scatter(x=ts,
                                y=zs,
                                name="Resistivity",
                                line=dict(color='black'),
                                mode='lines+markers',
                                # TODO: Wanted to add colorbar to the line, but this is non-trival. Must implement myselft
                                # if this is needed
                                # marker=dict(
                                #    color=[minValue, maxValue],
                                #    colorscale=colorScale,
                                #    colorbar=dict(thickness=10),
                                #    showscale=True
                                # ),
                                )

    rangeOfZs = maxValue - minValue
    yaxisPadding = rangeOfZs / 100 * 20

    linechart_layout = {
        'title': "Temporal changes in coord:" + str(x + 1) + " " + str(y + 1),
        'xaxis': {
            "side": "bottom",
            "type": "linear",
            # "range": [
            #    max(ts) - 30,
            #    max(ts) + 1
            # ],
        },
        'yaxis': {
            "side": "bottom",
            "type": "linear",
            # "range": [
            #    minValue - yaxisPadding,
            #    maxValue + yaxisPadding
            # ],
        },
        'ylabel': 'Resistivity (Ohm)'
    }

    linechart_fig = {
        'data': [linechart_data, keepTrackOfIteration],
        'layout': linechart_layout
    }
    return linechart_fig


def getTimeFormat(timeString):
    return datetime.datetime.strptime(timeString, "%H:%M:%S")
