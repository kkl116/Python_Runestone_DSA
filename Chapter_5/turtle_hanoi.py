# 12. Modify the Tower of Hanoi program using turtle graphics to animate the movement of the disks. 
# Hint: You can make multiple turtles and have them shaped like rectangles.
# animated_hanoi.py
from turtle import Turtle
from pythonds3 import Stack 

stack_dists = 225
stack_height = stack_dists*2

def init_poles():
    base = stack_dists//4
    vert = stack_height//2
    t = Turtle()
    t.speed('fastest')
    t.left(90)
    for i in range(3):
        t.up()
        t.goto((i-1)*stack_dists, 0)
        t.backward(vert)
        t.down()
        t.forward(vert)
        t.up()
        t.backward(vert)
        t.down()
        t.left(90)
        t.forward(base)
        t.up()
        t.backward(base)
        t.right(180)
        t.down()
        t.forward(base)
        t.left(90)
    t.hideturtle()

def get_next_y(stack):
    return (stack.size() * stack.h_dist) - stack_height//2 + stack.h_dist//2

def move_turtle(to_stack, from_stack):
    y_ceil = from_stack.n * from_stack.h_dist + stack_height//4
    top = from_stack.pop()
    top.up()
    top.goto((from_stack.x, y_ceil))
    top.goto((to_stack.x, y_ceil))
    top.goto((to_stack.x, get_next_y(to_stack)))
    to_stack.push(top)
    
def move_disk(from_stack, to_stack):
    print(f'moving from {from_stack.name} to {to_stack.name}')
    move_turtle(to_stack, from_stack)

def move_tower(n_disks, from_stack, to_stack, with_stack):
    if n_disks >= 1:
        #move tower of n-1 to with_stack, to free up bottom disk at from_stack
        move_tower(n_disks-1, from_stack, with_stack, to_stack)
        #move_disk from from_stack to to_stack
        move_disk(from_stack, to_stack)
        #move remaining tower from with_stack back to to_stack
        move_tower(n_disks-1, with_stack, to_stack, from_stack)

def hanoi_with_stacks(n, disk_w=0.5, disk_h=0.125):
    #initialize stacks
    stacks = [Stack() for _ in range(3)]
    for i, name in enumerate(['A', 'B', 'C']):
        stacks[i].name = name
        #set x coordinates for each pole 
        stacks[i].x = (i-1) * stack_dists
        #save n disks and h_dist (distance between disks) for later use - could pass it in to move_tower,
        #but this is slightly neater?
        #perhaps saving it as a class var is nicer but writing another class seems redundant
        stacks[i].n = n
        stacks[i].h_dist = 5

    init_poles()

    for i in range(n, 0, -1):
        #initialize turtles and move to stack_a
        t = Turtle(shape='square')
        t.hideturtle()
        t.speed('fast')
        #disk width slimmer on higher stacks
        t.turtlesize(disk_h, disk_w * (i), 1)
        t.up()
        t.goto((stacks[0].x, get_next_y(stacks[0])))
        t.showturtle()
        stacks[0].push(t)

    move_tower(n, *[stacks[0], stacks[2], stacks[1]])


if __name__ == '__main__':
    hanoi_with_stacks(4)