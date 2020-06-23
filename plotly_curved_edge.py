import numpy as np

## generate curved edge
def edge_curve(tgt_x, tgt_y, rlt_x, rlt_y, curve_dir, ratio = 0.2, marker_size = 15):
    ## target coords are the coords of source node
    ## relation coords are the coords of relation node
    ## curve_dir is the direction of the bent of the curve when we defines the [source node, relation node] as direction - to left or right
    ## ratio defines how bent the arc is
    ## marker_size helps to adjust edge position
    
    curve_dir = curve_dir.upper()
    dist = np.sqrt(np.power(tgt_x - rlt_x, 2) + np.power(tgt_y - rlt_y, 2))
    k = dist / 2 * np.tan(ratio * np.pi) 
    
    ## adjust with marker radius so that there is no overlap
    pxl_to_dist_r = marker_size * 0.0027
    
    if rlt_y > tgt_y:
        tgt_x = tgt_x - pxl_to_dist_r * (1 if curve_dir == "LEFT" else -1)
        rlt_x = rlt_x - pxl_to_dist_r * (1 if curve_dir == "LEFT" else -1)
        
    else:
        tgt_x = tgt_x - pxl_to_dist_r * (-1 if curve_dir == "LEFT" else 1)
        rlt_x = rlt_x - pxl_to_dist_r * (-1 if curve_dir == "LEFT" else 1)
    
    if rlt_x > tgt_x:
        tgt_y = tgt_y + pxl_to_dist_r * (1 if curve_dir == "LEFT" else -1)
        rlt_y = rlt_y + pxl_to_dist_r * (1 if curve_dir == "LEFT" else -1)
    else:
        tgt_y = tgt_y + pxl_to_dist_r * (-1 if curve_dir == "LEFT" else 1)
        rlt_y = rlt_y + pxl_to_dist_r * (-1 if curve_dir == "LEFT" else 1)
    
    ## middle point coords
    mid_x = tgt_x + (rlt_x - tgt_x) / 2.0
    mid_y = tgt_y + (rlt_y - tgt_y) / 2.0

    ## the perpendicular bisector line of target nodes and related nodes
    a = (tgt_x - rlt_x) / (rlt_y - tgt_y - 1e-5) ## gradient - modified in case 0
    b = mid_y - a * mid_x ## intersect

    ## we want a point which is
        ## the top of the arc of the curved edge
        ## on the perpendicular bisector

    mid_x_adj = np.sqrt(np.power(k, 2) / (np.power(a, 2) + 1))

    if rlt_y > tgt_y:
        arc_x = mid_x - mid_x_adj * (1 if curve_dir == "LEFT" else -1)
    else:
        arc_x = mid_x - mid_x_adj * (-1 if curve_dir == "LEFT" else 1)
    arc_y = a * arc_x + b
    
    ## find the circle that goes through target nodes, related nodes and arc top nodes
    params = np.array([[2 * tgt_x, 2 * tgt_y, 1],\
                       [2 * rlt_x, 2 * rlt_y, 1],\
                       [2 * arc_x, 2 * arc_y, 1]])
    res = np.array([-np.power(tgt_x, 2) - np.power(tgt_y, 2),\
                    -np.power(rlt_x, 2) - np.power(rlt_y, 2),\
                    -np.power(arc_x, 2) - np.power(arc_y, 2)])

    a2, b2, _ = np.linalg.solve(params, res)

    ## x, y coords of center and radius
    ctr_x = - a2
    ctr_y = - b2
    r = np.sqrt(np.power(tgt_x - ctr_x, 2) + np.power(tgt_y - ctr_y, 2))
    
    ## find the radian of target and related node, starting counter-clockwise from positive x
    tgt_radian_x_pos_acute = np.arccos(round(tgt_x - ctr_x, 5) / r)
    tgt_radian = tgt_radian_x_pos_acute if tgt_y > ctr_y else 2 * np.pi - tgt_radian_x_pos_acute
    
    arc_radian_x_pos_acute = np.arccos(round(arc_x - ctr_x, 5) / r)
    arc_radian = arc_radian_x_pos_acute if arc_y > ctr_y else 2 * np.pi - arc_radian_x_pos_acute
    
    rlt_radian_x_pos_acute = np.arccos(round(rlt_x - ctr_x, 5) / r)
    rlt_radian = rlt_radian_x_pos_acute if rlt_y > ctr_y else 2 * np.pi - rlt_radian_x_pos_acute
    
    radian_min = np.amin([tgt_radian, rlt_radian])
    radian_max = np.amax([tgt_radian, rlt_radian])
    
    ## arc should always between the target and relation radian, or we should increase the smaller one by 2 pi
    if not (radian_min < arc_radian < radian_max):
        radian_min = radian_min + 2 * np.pi
    
    ## array of 100 increasing radian
    radian_arr = np.linspace(radian_min, radian_max, 100)
    
    ## find coords of these points on curved edge
    edge_x_all = np.cos(radian_arr) * r + ctr_x
    edge_y_all = np.sin(radian_arr) * r + ctr_y
    
    return edge_x_all, edge_y_all
