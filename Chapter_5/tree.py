import random 
import turtle 

def tree(branch_len, t):
    leaf_thresh = 15
    if branch_len > 5:
        # 3.1 line width as a function of branch_len
        t.width(branch_len/20)
        # 3.2 change color of pen if branch_len is < thresh
        if branch_len < leaf_thresh:
            t.color('green')

        t.forward(branch_len)
        # 3.3 choose random angle at each turn
        ang = random.randrange(10, 31)
        # 3.4 choose random subtraction distance
        sub = random.randrange(5, 21)
        t.right(ang)
        tree(branch_len - sub, t)
        t.left(ang*2)
        tree(branch_len - sub, t)
        t.right(ang)
        if branch_len > leaf_thresh:
            # change color back to brown if at non-leaf
            # so backwards trace is correct color 
            t.color('brown')
        t.backward(branch_len)

def draw_tree():
    t = turtle.Turtle()
    my_win = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    t.color("brown")
    t.speed(8)
    tree(75, t)
    my_win.exitonclick()
    

if __name__ == '__main__': 
    draw_tree()