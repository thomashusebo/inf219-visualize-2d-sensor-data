import plotly.graph_objects as go


def getHeatMap(
        data,
        timestamp,
        colorScale,
        figure_type,
        coordinates=None,
        background_color='white',
        custom_color_range=None,
        figure_height=300,
        title="",
        axis_name=True,
        allow_lasso=True):

    half_cell_size = 0.5
    cell_length_meter = 0.2

    get_figure = {
        'heatmap': go.Heatmap,
        'contour': go.Contour,
        'surface': go.Surface
    }

    heatmap_fig = go.Figure()

    if len(data) == 0:
        return {
            'data': [],
            'layout': go.Layout(
                title=go.layout.Title(text=title+': No data found'),
                height=figure_height
            )
        }

    heatmap_fig, height, width = add_traces(colorScale, coordinates, custom_color_range, data, figure_type, get_figure,
                               half_cell_size, heatmap_fig)

    if axis_name:
        axis_title='meter'
    else:
        axis_title=None

    if allow_lasso:
        drag_mode = 'lasso'
    else:
        drag_mode = False

    heatmap_fig.update_layout(
        title=title,
        dragmode=drag_mode,
        xaxis=dict(
            range=[-half_cell_size, width - half_cell_size],
            constrain='domain',
            # side='top',
            tickmode='array',
            tickvals=[x - half_cell_size for x in list(range(width + 1))],
            ticktext=["{:.1f}".format(cell_length_meter * x) for x in range(width + 1)],
            tickangle=-45,
            showgrid=False,
            showline=False,
            zeroline=False,
            title=axis_title,

        ),
        yaxis=dict(
            range=[-half_cell_size, height - half_cell_size],
            # autorange='reversed',
            scaleanchor="x",
            scaleratio=1,
            constrain='domain',
            automargin=True,
            tickmode='array',
            tickvals=[x - half_cell_size for x in list(range(height + 1))],
            ticktext=["{:.1f}".format(cell_length_meter * x) for x in range(height + 1)],
            showgrid=False,
            showline=False,
            zeroline=False,
            title=axis_title,
        ),
        margin=dict(
            l=15,
            r=0,
            t=25,
            b=0,
            pad=0
        ),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        height=figure_height,
    )

    return heatmap_fig


def add_traces(colorScale, coordinates, custom_color_range, data, figure_type, get_figure, half_cell_size, heatmap_fig):
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
            zauto=not any([custom_color_range[x] for x in custom_color_range]),
            zmax=custom_color_range['max'],
            zmin=custom_color_range['min'],
            colorbar=dict(
                len=1
            ),
            # contours_coloring='heatmap'
        ),
    )
    if coordinates:
        for coordinate in coordinates:
            heatmap_fig.add_shape(
                type="rect",
                x0=coordinate['x'] - half_cell_size,
                y0=coordinate['y'] - half_cell_size,
                x1=coordinate['x'] + half_cell_size,
                y1=coordinate['y'] + half_cell_size)
    return heatmap_fig, height, width
