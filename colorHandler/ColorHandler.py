
# Colorblind scales, divergent, 11 colors
colorblindsafe = {
    'divergent':{
        11:{    # 11 colors
            1:['#a50026','#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695'],
            2:['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061'],
            3:['#7f3b08','#b35806','#e08214','#fdb863','#fee0b6','#f7f7f7','#d8daeb','#b2abd2','#8073ac','#542788','#2d004b'],
            4:['#40004b','#762a83','#9970ab','#c2a5cf','#e7d4e8','#f7f7f7','#d9f0d3','#a6dba0','#5aae61','#1b7837','#00441b'],
            5:['#8e0152','#c51b7d','#de77ae','#f1b6da','#fde0ef','#f7f7f7','#e6f5d0','#b8e186','#7fbc41','#4d9221','#276419'],
            6:['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#f5f5f5','#c7eae5','#80cdc1','#35978f','#01665e','#003c30']
        }
    }
}


def getColorScale():
    # Get Colors
    n_colors = 11
    scaletype = 'divergent'
    colors = colorblindsafe[scaletype][n_colors][2]

    # Define stepsize
    stepsize = 1/(len(colors)-1)
    colorMap = [[round(i*stepsize, 1), colors[i]] for i in range(len(colors))]

    return colorMap

