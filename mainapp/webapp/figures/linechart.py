import plotly.graph_objects as go
import plotly.express as px


def getLineChart(data, timestamp, coordinate, colorScale, timeline):
    if len(data) < 1: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

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
