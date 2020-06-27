import plotly.graph_objects as go
import plotly.express as px


def getLineChart(data, timestamp, coordinates, colorScale, timeline):
    if len(data) < 1: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

    x = data.iloc[:, 0].values

    linechart_fig = go.Figure()

    means = data.iloc[:, 1:].transpose().mean().transpose()
    var=data.iloc[:,1:].transpose().std().transpose()

    up = means + var
    down = means - var


    if data.shape[1] > 1:
        linechart_fig.add_trace(go.Scatter(
            x=x,
            y=means,
            mode='lines+markers',
            line=dict(
                color=colorScale[0][1],
                width=2
            ),
            marker=dict(
                color=colorScale[0][1],
                size=2
            )
        ))

    if data.shape[1] > 2:
        linechart_fig.add_trace(go.Scatter(
            x=x,
            y=down,
            mode='lines',
            line=dict(width=1, color='black'),
        ))

        linechart_fig.add_trace(go.Scatter(
            name='Upper Bound',
            x=x,
            y=up,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=1, color='black'),
            fillcolor=colorScale[round(len(colorScale)/2)][1],
            fill='tonexty'))

    ys = data.shape[1]
    for y in range(1, ys):
        y = data.iloc[:, y].values
        linechart_fig.add_trace(go.Scatter(x=x,
                                           y=y,
                                           mode='lines+markers',
                                           line=dict(color='grey')))

    linechart_fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            range=[timeline['start'], timeline['end']],
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
        plot_bgcolor='white',
        dragmode='pan'
    )

    return linechart_fig
