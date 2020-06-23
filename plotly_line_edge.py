import numpy as np

## generate straight edge
def edge_line(tgt_x, tgt_y, rlt_x, rlt_y, marker_size = 15):
    ## adjust with marker radius so that there is no overlap
    pxl_to_dist_r = marker_size * 0.0027 / 2
    
    a = (rlt_y - tgt_y) / (rlt_x - tgt_x + 1e-3)
    b = rlt_y - a * rlt_x
    
    if rlt_x != tgt_x:
        tgt_x = tgt_x + pxl_to_dist_r * (1 if rlt_x > tgt_x else -1)
        rlt_x = rlt_x - pxl_to_dist_r * (1 if rlt_x > tgt_x else -1)
    ## else no adjustment
    
    tgt_y = a * tgt_x + b
    rlt_y = a * rlt_x + b
    
    if rlt_x != tgt_x:
        a = (rlt_y - tgt_y) / (rlt_x - tgt_x)
        b = rlt_y - a * rlt_x
        edge_x_all = np.linspace(tgt_x, rlt_x, 100)
        edge_y_all = a * edge_x_all + b
    else:
        edge_x_all = np.empty(100); edge_x_all.fill(tgt_x)
        edge_y_all = np.linspace(tgt_y, rlt_y, 100)
        
    return edge_x_all, edge_y_all
