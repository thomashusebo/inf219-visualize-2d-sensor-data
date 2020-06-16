import plotly.graph_objects as go


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

    # TODO: Add timestamp to linechart
    #firstTimeStamp = data[0]['ts'][0][0]
    #projectStartTime = datetime.datetime.strptime(firstTimeStamp, "%H:%M:%S")

    # ts = [getTimeFormat(data[i]['ts'][y][x]) - projectStartTime for i in range(len(data))]

    keepTrackOfIteration = go.Scatter(x=[iterationID, iterationID],
                                      y=[0, zs[iterationID]],
                                      name="Timestep",
                                      line=dict(color='black'),
                                      )

    linechart_data = go.Scatter(x=ts,
                                y=zs,
                                name="Resistivity",
                                line=dict(color='black'),
                                mode='markers',
                                # TODO: Wanted to add colorbar to the line, but this is non-trival. Must implement myselft
                                # if this is needed
                                #marker=dict(
                                #    color=[minValue, maxValue],
                                #    colorscale=colorScale,
                                #    colorbar=dict(thickness=10),
                                #    showscale=True
                                #),
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
            "title": "Measurement",
        },
        'yaxis': {
            "side": "bottom",
            "type": "linear",
            #"range": [
            #    minValue - yaxisPadding,
            #    maxValue + yaxisPadding
             #],
            "title":'Resistivity (Ohm)'
        },
    }

    linechart_fig = {
        'data': [linechart_data, keepTrackOfIteration],
        'layout': linechart_layout
    }
    return linechart_fig