def build_break_style_info(style):
    import numpy as np
    style_length = 0
    style_points = []
    mul = 1
    for char in style:
        if char.isdigit():
            mul = int(char)
            continue
        if char == "^":
            sz = 2
            pts = [[0.0,0.0],[1.0,1.0],[2.0,0.0]]
        if char == "/":
            sz = 1
            pts = [[0.0,0.0],[1.0,1.0]]
        if char == "\\":
            sz = 1
            pts = [[0.0,1.0],[1.0,0.0]]
        if char == "~":
            sz = 2*np.pi
            x = np.linspace(0, sz, 31)
            y = (np.sin(x - np.pi/2) + 1)/2
            pts = list(zip(x,y))
        if char == "-":
            sz = 1
            pts = [[0.0,1.0],[1.0,1.0]]
        if char == " ":
            sz = 1
            pts = [[0.0,0.0],[1.0,0.0]]
        if char == " " or char == "_":
            sz = 1
            pts = [[0.0,0.0],[1.0,0.0]]
        style_points.extend(map(list, np.array(pts)*(mul,1) + [style_length, 0]))
        style_length += sz*mul
        mul = 1
    return np.array(style_points)*(1/style_length, 1)

