
# Colorblind scales, divergent, 11 colors
colorblindsafe = {
    'divergent':{
        11:{    # 11 colors
            "red-yellow-blue":['#313695','#4575b4','#74add1','#abd9e9','#e0f3f8','#ffffbf','#fee090','#fdae61','#f46d43','#d73027','#a50026'],
            "red-white-blue":['#053061','#2166ac','#4393c3','#92c5de','#d1e5f0','#f7f7f7','#fddbc7','#f4a582','#d6604d','#b2182b','#67001f'],
            "purple-orange":['#7f3b08','#b35806','#e08214','#fdb863','#fee0b6','#f7f7f7','#d8daeb','#b2abd2','#8073ac','#542788','#2d004b'],
            "green-purple":['#40004b','#762a83','#9970ab','#c2a5cf','#e7d4e8','#f7f7f7','#d9f0d3','#a6dba0','#5aae61','#1b7837','#00441b'],
            "green-pink":['#8e0152','#c51b7d','#de77ae','#f1b6da','#fde0ef','#f7f7f7','#e6f5d0','#b8e186','#7fbc41','#4d9221','#276419'],
            "green-yellow":['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#f5f5f5','#c7eae5','#80cdc1','#35978f','#01665e','#003c30']
        }
    }
}


def getColorScale(type):
    # Get Colors
    n_colors = 11
    scaletype = 'divergent'
    colors = colorblindsafe[scaletype][n_colors][type]

    # Define stepsize
    stepsize = 1/(len(colors)-1)
    colorMap = [[round(i*stepsize, 1), colors[i]] for i in range(len(colors))]

    return colorMap

