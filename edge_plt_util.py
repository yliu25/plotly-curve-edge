#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

#%% generate curved edge
def edge_curve(tgt_x, tgt_y, rlt_x, rlt_y, curve_dir, k = 0.8):
    ## k defines how curved the edge is
    
    curve_dir = curve_dir.upper()
    
    ## middle point coords
    mid_x = tgt_x + (rlt_x - tgt_x) / 2.0
    mid_y = tgt_y + (rlt_y - tgt_y) / 2.0

    ## the perpendicular bisector line of target type nodes and related type nodes
    a = 0 if rlt_x == tgt_x else (tgt_x - rlt_x) / (rlt_y - tgt_y) ## gradient
    b = mid_y - a * mid_x ## intersect

    ## we want a point which is
        ## the top of the arc of the curved edge
        ## on the perpendicular bisector
    
    arc_x = mid_x - np.sqrt(np.power(k, 2) / (np.power(a, 2) + 1)) * (1 if curve_dir == "LEFT" else -1)
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
    if tgt_y <= ctr_y:
        tgt_radian = 2 * np.pi - np.arccos((tgt_x - ctr_x) / r)
    else:
        tgt_radian = np.pi * (0 if curve_dir == "LEFT" else 2) + np.arccos((tgt_x - ctr_x) / r)

    if rlt_y <= ctr_y:
        rlt_radian = 2 * np.pi - np.arccos((rlt_x - ctr_x) / r)
    else:
        rlt_radian = np.pi * (0 if curve_dir == "LEFT" else 2) + np.arccos((rlt_x - ctr_x) / r)

    ## array of 100 increasing radian
    radian_arr = np.linspace(tgt_radian, rlt_radian, 100)
    ## find coords of these points on curved edge
    edge_x_all = np.cos(radian_arr) * r + ctr_x
    edge_y_all = np.sin(radian_arr) * r + ctr_y
    
    return edge_x_all, edge_y_all

#%% generate straight edge
def edge_line(tgt_x, tgt_y, rlt_x, rlt_y):
    if rlt_x != tgt_x:
        a = (rlt_y - tgt_y) / (rlt_x - tgt_x)
        b = rlt_y - a * rlt_x
        edge_x_all = np.linspace(tgt_x, rlt_x, 100)
        edge_y_all = a * edge_x_all + b
    else:
        edge_x_all = np.empty(100); edge_x_all.fill(tgt_x)
        edge_y_all = np.linspace(tgt_y, rlt_y, 100)
        
    return edge_x_all, edge_y_all