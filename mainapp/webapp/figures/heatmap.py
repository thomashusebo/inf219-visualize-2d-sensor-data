from plotly.subplots import make_subplots
import plotly.graph_objects as go


def getHeatMap(data, timestamp, colorScale, figure_type, coordinates=None):
    get_figure = {
        'heatmap': go.Heatmap,
        'contour': go.Contour,
        'surface': go.Surface
    }

    if len(data) == 0: return {
        'data': [],
        'layout': go.Layout(title=go.layout.Title(text='No data found'))
    }

    heatmap_fig = go.Figure()

    height, width = data.shape

    heatmap_fig.add_trace(
        go.Scatter(
            x=[i for i in range(width) for j in range(height)],
            y=[j for i in range(width) for j in range(height)],
            mode='markers',
            marker=dict(
                size=2,
                color='black'
            )
        )
    )

    heatmap_fig.add_trace(
        get_figure[figure_type](
            z=data,
            colorscale=colorScale,
            colorbar=dict(
                len=0.8,
            ),
        ),
    )

    if coordinates:
        for coordinate in coordinates:
            heatmap_fig.add_shape(
                type="rect",
                x0=coordinate['x']-0.5,
                y0=coordinate['y']-0.5,
                x1=coordinate['x']+0.5,
                y1=coordinate['y']+0.5)

    heatmap_fig.update_layout(
        dragmode='lasso',
        xaxis=dict(
            range=[-0.5, width-0.5],
            constrain='domain'
        ),
        yaxis=dict(
            range=[-0.5, height-0.5],
            scaleanchor="x",
            scaleratio=1,
            constrain='domain',
            automargin=True,
        ),
        margin=dict(
            l=15,
            r=0,
            t=0,
            b=0,
            pad=0
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        height=300,
    )

    return heatmap_fig


