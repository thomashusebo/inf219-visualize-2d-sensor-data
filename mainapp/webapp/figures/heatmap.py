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

    heatmap_fig.add_trace(go.Scatter(
        x=[i for i in range(width) for j in range(height)],
        y=[j for i in range(width) for j in range(height)],
        mode='markers',
        marker=dict(
            size=2,
            color='black'
        )))

    heatmap_fig.add_trace(get_figure[figure_type](z=data, colorscale=colorScale))

    if coordinates:
        for coordinate in coordinates:
            heatmap_fig.add_shape(
                type="rect",
                x0=coordinate['x']-0.5,
                y0=coordinate['y']-0.5,
                x1=coordinate['x']+0.5,
                y1=coordinate['y']+0.5)

    heatmap_fig.update_layout(
        title="Resistivity heatmap: {}".format(timestamp),
        dragmode='lasso',
        xaxis=dict(
            fixedrange=True
        ),
        yaxis=dict(
            scaleanchor = "x",
            scaleratio=1,
            fixedrange=True
        ),
        margin=dict(
            l=40,
            r=40,
            t=40,
            b=25,
        ),
    )
    return heatmap_fig


