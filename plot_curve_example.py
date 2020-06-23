import numpy as np

np.random.seed(22)
tgt_x, tgt_y = np.random.uniform(-1, 1, (2, 1))

## generate a point below
blw_x, blw_y = tgt_x, tgt_y - 1.0

## generate a point to the right
right_x, right_y = tgt_x + 1.0, tgt_y

## generate a random point
rand_x, rand_y = np.random.uniform(-1, 1, (2, 1))

dir_x, dir_y = np.concatenate((blw_x, right_x, rand_x)), np.concatenate((blw_y, right_y, rand_y))

nodes_trace = []
nodes_trace.append(go.Scatter(x = tgt_x, y = tgt_y, name = "previous node",
                              mode = "markers", marker = {"size": 20, "color": "blue"}))
nodes_trace.append(go.Scatter(x = dir_x, y = dir_y, name = "next node",
                              mode = "markers", marker = {"size": 20, "color": "red"}))

edges_trace = []
edges_anno = []

## for point below
edge_x, edge_y = edge_curve(tgt_x[0], tgt_y[0], blw_x[0], blw_y[0],
                            curve_dir = "right", ratio = 0.1, marker_size = 20)
edges_trace.append(go.Scatter(x = edge_x, y = edge_y, mode = "lines",
                              line = {"color": "gray"}, showlegend = False))
edges_anno.append(dict(x = edge_x[-50], y = edge_y[-50], xref = "x", yref = "y",
                       showarrow = True,
                       ax = edge_x[-60], ay = edge_y[-60], axref = "x", ayref = "y",
                       arrowhead = 3, arrowwidth = 3, arrowcolor = "gray"))

edge_x, edge_y = edge_curve(blw_x[0], blw_y[0], tgt_x[0], tgt_y[0],
                            curve_dir = "right", ratio = 0.1, marker_size = 20)
edges_trace.append(go.Scatter(x = edge_x, y = edge_y, mode = "lines",
                              line = {"color": "gray"}, showlegend = False))
edges_anno.append(dict(x = edge_x[-50], y = edge_y[-50], xref = "x", yref = "y",
                       showarrow = True,
                       ax = edge_x[-60], ay = edge_y[-60], axref = "x", ayref = "y",
                       arrowhead = 3, arrowwidth = 3, arrowcolor = "gray"))

## for point on the right
edge_x, edge_y = edge_curve(tgt_x[0], tgt_y[0], right_x[0], right_y[0],
                            curve_dir = "left", ratio = 0.1, marker_size = 20)
edges_trace.append(go.Scatter(x = edge_x, y = edge_y, mode = "lines",
                              line = {"color": "gray"}, showlegend = False))
edges_anno.append(dict(x = edge_x[-50], y = edge_y[-50], xref = "x", yref = "y",
                       showarrow = True,
                       ax = edge_x[-60], ay = edge_y[-60], axref = "x", ayref = "y",
                       arrowhead = 3, arrowwidth = 3, arrowcolor = "gray"))

edge_x, edge_y = edge_curve(right_x[0], right_y[0], tgt_x[0], tgt_y[0],
                            curve_dir = "left", ratio = 0.1, marker_size = 20)
edges_trace.append(go.Scatter(x = edge_x, y = edge_y, mode = "lines",
                              line = {"color": "gray"}, showlegend = False))
edges_anno.append(dict(x = edge_x[-50], y = edge_y[-50], xref = "x", yref = "y",
                       showarrow = True,
                       ax = edge_x[-60], ay = edge_y[-60], axref = "x", ayref = "y",
                       arrowhead = 3, arrowwidth = 3, arrowcolor = "gray"))

## for random point
edge_x, edge_y = edge_line(tgt_x[0], tgt_y[0], rand_x[0], rand_y[0], marker_size = 20)
edges_trace.append(go.Scatter(x = edge_x, y = edge_y, mode = "lines",
                              line = {"color": "gray"}, showlegend = False))
edges_anno.append(dict(x = edge_x[-40], y = edge_y[-40], xref = "x", yref = "y",
                       showarrow = True,
                       ax = edge_x[-60], ay = edge_y[-60], axref = "x", ayref = "y",
                       arrowhead = 3, arrowwidth = 3, arrowcolor = "gray"))
    
fig = go.Figure(data = edges_trace + nodes_trace)

fig.update_xaxes(showticklabels = False, showgrid = False, zeroline = False)
fig.update_yaxes(showticklabels = False, showgrid = False, zeroline = False)
    
fig.update_layout(yaxis = dict(scaleanchor = "x", scaleratio = 1),
                  showlegend = False,
                  width = 500, height = 500, margin = {"l": 5, "r": 5, "t": 5, "b": 5},
                  annotations = edges_anno,
                  plot_bgcolor = "white")
