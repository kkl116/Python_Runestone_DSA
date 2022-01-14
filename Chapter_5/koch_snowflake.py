import turtle 
import math

def connect_pts(pts, t):
    t.up()
    for i,c in enumerate(pts):
        if i > 0:
            t.down()
        t.goto(c)
    return 

def get_dist(p1 ,p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[0])**2)

def get_tri_coords(centre, dist):
    p1 = [centre[0] - dist//2, centre[1] - dist * (math.sqrt(3)/4) ]
    p2 = [centre[0], centre[1] + dist * (math.sqrt(3)/4)]
    p3 = [centre[0] + dist//2, centre[1] - dist * (math.sqrt(3)/4) ]
    return p1, p2, p3 

def get_third_coord(p1, p3):
    #https://www.khanacademy.org/computing/pixar/sets/rotation/v/set-7
    angle = 60
    #rotate p3 about p1 - first subtract p1 from p3 
    a = math.radians(angle)
    ox, oy = p1 
    px, py = p3 
    #set p1 as origin
    px_o, py_o = px-ox, py-oy 
    #rotate point 
    qx = (math.cos(a) * px_o) - (math.sin(a) * py_o)
    qy = (math.sin(a) * px_o) + (math.cos(a) * py_o)
    return [qx + ox, qy + oy] 

def get_middle_seg(p1, p2):
    #split line into 3 and get middle start and end 
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    start = p1[0] + x_diff/3, p1[1] + y_diff/3
    end = p1[0] + x_diff*(2/3), p1[1] + y_diff*(2/3)
    return start, end 

def koch_snowflake(k, pts):
    if k == 0:
        return pts
    if k >= 1:
        #between each pair of points, find middle seg and cooresponding third coord
        new_pts = []
        for i in range(1, len(pts)):
            #for each pair of points find mid seg and third coord?
            mid_seg = get_middle_seg(pts[i-1], pts[i])
            third = get_third_coord(mid_seg[0], mid_seg[1])
            new_pts.append(pts[i-1])
            new_pts.append(mid_seg[0])
            new_pts.append(third)
            new_pts.append(mid_seg[1])
        
        #append final point
        new_pts.append(pts[-1])
        #call next degree koch snowflake 
        return koch_snowflake(k-1, new_pts)
    

def draw_snowflake(k):
    win_len = 550
    turtle.screensize(canvwidth=win_len, canvheight=win_len)
    turtle.setworldcoordinates(-win_len//2, -win_len//2, win_len//2, win_len//2)
    t = turtle.Turtle()
    my_win = turtle.Screen()
    t.speed(5)
    t.up()

    start_point = [0, 0]
    snowflake_len = 3**5

    init_pts = get_tri_coords(start_point, snowflake_len)
    init_coords = [[init_pts[0], init_pts[1]], [init_pts[1], init_pts[2]], [init_pts[2], init_pts[0]]]

    #do one side of koch snowflake at a time! they don't have to be done together
    for coords in init_coords:
        points = koch_snowflake(k, coords)
        connect_pts(points, t)
    my_win.exitonclick()

if __name__ == '__main__':
    draw_snowflake(4)