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
    var = data.iloc[:, 1:].transpose().std().transpose()

    # Add continuous error bars to the plot
    error_colors = ['#d9d9d9', '#bdbdbd', '#969696']
    for i in reversed(range(1, 4)):
        fill_color = error_colors[i-1]
        if data.shape[1] > 2:
            linechart_fig.add_trace(go.Scatter(
                x=x,
                y=means - i * var,
                mode='lines',
                line=dict(width=1, color='black'),
                showlegend=False
            ))

            linechart_fig.add_trace(go.Scatter(
                name='{} sigma'.format(i),
                x=x,
                y=means + i * var,
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=1, color='black'),
                fillcolor=fill_color,
                fill='tonexty'))

    # Add induvidual traces to the plot
    '''ys = data.shape[1]
    for y in range(1, ys):
        y = data.iloc[:, y].values
        linechart_fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            line=dict(
                width=1,
                color='#f0f0f0'),
            marker=dict(
                size=2,
                color='#f0f0f0'),
            showlegend=False
        ))'''

    # Add central values to the plot
    if data.shape[1] > 1:
        if data.shape[1] == 2:
            trace_name = '[{:d},{:d}]'.format(coordinates[0]['x'], coordinates[0]['y'])
        else:
            trace_name = 'Average'

        linechart_fig.add_trace(go.Scatter(
            name=trace_name,
            x=x,
            y=means,
            mode='lines+markers',
            line=dict(
                color='#292929',
                width=1
            ),
            marker=dict(
                color='#292929',
                size=3
            ),
            showlegend=True
        ))

    # Add vertical line representing selected timestamp
    linechart_fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            yref='paper',
            x0=timestamp,
            y0=0,
            x1=timestamp,
            y1=1,
            line=dict(
                color="black",
                width=2
            ),
        ))

    linechart_fig.update_layout(
        xaxis=dict(
            range=[timeline['start'], timeline['end']],
            type="date",
            linecolor='black',
            gridcolor='LightGrey'
        ),
        yaxis=dict(
            title='Resistivity (Ohm)',
            rangemode='tozero',
            linecolor='black',
            gridcolor='LightGrey',
            fixedrange=True
        ),
        margin=dict(
            l=15,
            r=0,
            t=15,
            b=5,
            pad=0
        ),
        plot_bgcolor='white',
        dragmode=False,
        height=250,
    )

    return linechart_fig
