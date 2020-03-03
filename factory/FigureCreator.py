import plotly.graph_objects as go
import plotly.express as px


def getHeatMap(data, iterationID, color_scale):
    oneFrame = data[iterationID]
    xs = oneFrame['xs']
    ys = oneFrame['ys']
    zs = oneFrame['zs']

    heatmap_data = go.Heatmap(x=xs,
                              y=ys,
                              z=zs,
                              colorscale=color_scale
                              )
    heatmap_layout = go.Layout(title=go.layout.Title(text='Resistivity heatmap'))

    heatmap_fig = {
        'data': [heatmap_data],
        'layout': heatmap_layout}

    return heatmap_fig


def getLineChart(data, iterationID, coordinate, color_scale):
    x = coordinate['x']
    y = coordinate['y']
    ts = [i for i in range(len(data))]
    zs = [data[i]['zs'][x][y] for i in range(len(data))]
    #linechart_data = px.line(
    #                        x=ts,
    #                        y=zs
    #)

    keepTrackOfIteration = go.Scatter(x=[iterationID,iterationID],
                                      y=[0,zs[iterationID]],
                                      name="Current iteration viewed in heatmap",
                                      line=dict(color=color_scale[10][1])
                                      )

    linechart_data = go.Scatter(x=ts,
                                y=zs,
                                name="Resistivity",
                                line=dict(color=color_scale[0][1])
                               )

    linechart_layout = go.Layout(title=go.layout.Title(text="Temporal changes in coord:" + str(x) + " " + str(y)))
    linechart_fig = {
        'data': [linechart_data, keepTrackOfIteration],
        'layout': linechart_layout
    }
    return linechart_fig