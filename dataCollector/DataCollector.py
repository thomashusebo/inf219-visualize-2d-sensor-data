def getData():
    data = {}
    n = 14  # number of columns
    m = 7  # number of rows
    for t in range(10):
        xs = [i for i in range(1, n + 1)]  # Defines x's
        ys = [i for i in range(1, m + 1)]  # Defines y's
        zs = [[t ** 2 + (i * j) for i in xs] for j in ys]  # Defines plotted value in heatmap, product of x and y

        data[t] = {
            'xs': xs,
            'ys': ys,
            'zs': zs
        }

    return data
