import turtle
import math

#https://github.com/MollyZhang/Algorithm-and-Data-Structure-In-Python/blob/master/Recursion-exercise3-hilbert%20curve.py
#above link helped clarify approach to draw from coordinates

#7. Using the turtle graphics module, write a recursive program to display a Hilbert curve.
def get_midpoint(p1, p2):
    return (p1[0] + p2[0])//2, (p1[1] + p2[1])//2

def get_u_coords(p1, p2, p3, p4):
    #from coordinates of the main sqaure, gets points within the quadrants for the u
    mid = get_midpoint(p1, p3)
    q1 = get_midpoint(p1, mid)
    q2 = get_midpoint(p2, mid)
    q3 = get_midpoint(p3, mid)
    q4 = get_midpoint(p4, mid)
    
    return [q1, q2, q3, q4]

def connect_pts(pts, t):
    t.up()
    for i,c in enumerate(pts):
        if i > 0:
            t.down()
        t.goto(c)
    return 

def get_quadrants(p1, p2, p3, p4):
    #get coordinates to split four quadrants 
    quad1 = [p1, get_midpoint(p1, p2), get_midpoint(p1, p3), get_midpoint(p1, p4)]
    quad2 = [get_midpoint(p1, p2), p2, get_midpoint(p2, p3), get_midpoint(p2, p4)]
    quad3 = [get_midpoint(p1, p3), get_midpoint(p2, p3), p3, get_midpoint(p3, p4)]
    quad4=  [get_midpoint(p1, p4), get_midpoint(p2, p4), get_midpoint(p3, p4), p4]
    return [quad1, quad2, quad3, quad4]

def rotate(coords, n=1):
    assert n == 1 or n == 3
    #1 n is -90 degrees
    if n == 1:
        return [coords[0], coords[3], coords[2], coords[1]]
    if n == 3:
        return [coords[2], coords[1], coords[0], coords[3]]

#key 1: collate all points and connect at the END!
#key_2: was working with upside down u at first so transposes were all wrong 
#key_3: rotate quadrant 1 by -90 and quadrant 4 by -270 each iteration, but the ORDER of the points is important... 
# ---- think of how you'd draw an order 2 curve, and think of the order of the points!
def hilbert(k, p1, p2, p3, p4, t):
    #I think first thing is to calculate coordinates of the global quadrant...
    if k == 1:
        return get_u_coords(p1, p2, p3, p4)
    if k > 1:
        points = []
        #split current points into four quadrants, and draw u in each 
        quadrants = get_quadrants(p1, p2, p3, p4)
        for i, q in enumerate(quadrants):
            #need to figure out what's happening here...
            if i == 0:
                q = rotate(q, 1)
            elif i == 3:
                q = rotate(q, 3)
            points = points + hilbert(k-1, *q, t)
        return points
    

def draw_hilbert(k):
    win_len = 550
    bound_len = 512
    turtle.screensize(canvwidth=win_len, canvheight=win_len)
    turtle.setworldcoordinates(bound_len - win_len, bound_len - win_len, win_len, win_len)
    t = turtle.Turtle()
    my_win = turtle.Screen()
    t.hideturtle()
    t.speed('fastest')
    t.left(90)
    t.up()
    t.goto((0, bound_len))
    colors = ['#122c91', '#2a6fdb', '#48d6d2', 'orange', '#0a2f35', '#fefcbf', 'purple', 'gold']
    for k, col in zip(range(1, k+1), colors):
        t.color(col)
        points = hilbert(k, [0, bound_len], [0, 0], [bound_len, 0], [bound_len, bound_len], t)
        connect_pts(points, t)
    my_win.exitonclick()

if __name__ == '__main__':
    draw_hilbert(6)

