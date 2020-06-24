import plotly.graph_objects as go
import plotly.express as px


def getLineChart(data, timestamp, coordinate, colorScale, timeline):
    if len(data) < 1: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

    '''x = coordinate['x']
    y = coordinate['y']

    # TODO: Add timestamp to linechart
    keepTrackOfIteration = go.Scatter(x=[timestamp,timestamp],
                                      y=[0,1000],
                                      name="Timestep",
                                      line=dict(color='black'),
                                      )

    linechart_data = go.Scatter(x=data[data.columns[0]],
                                y=data[data.columns[1]],
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

    #rangeOfZs = maxValue - minValue
    #yaxisPadding = rangeOfZs / 100 * 20

    linechart_layout = {
        'title': "Temporal changes in coord:" + str(x) + " " + str(y),
        'xaxis': {
            "side": "bottom",
            "type": "linear",
            "title": "Measurement",
        },
        'yaxis': {
            "side": "bottom",
            "type": "linear",
            "title":'Resistivity (Ohm)'
        },
    }

    linechart_fig = {
        'data': [linechart_data, keepTrackOfIteration],
        'layout': linechart_layout
    }'''

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    linechart_fig = go.Figure(data=go.Scatter(x=x, y=y,
                                              mode='lines+markers'))
    linechart_fig.update_layout(
        title="Temporal changes in coord: " + str(coordinate['x']) + " " + str(coordinate['y']),
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            range=[timeline['start'],timeline['end']],
            type="date",
            linecolor='black',
            gridcolor='LightGrey'
        ),
        yaxis=dict(
            title='Resistivity (Ohm)',
            rangemode='tozero',
            linecolor='black',
            gridcolor='LightGrey'
        ),
        plot_bgcolor='white'
    )

    return linechart_fig
