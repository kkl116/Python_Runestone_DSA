#GUI to allow user to enter current sudoku for solving
import numpy as np 
import pygame 
import sys
from button import Button
from solver import solve_sudoku

board_dims = (550, 600)
background_color = (255, 255, 255)
user_elem_color = (65, 105, 225)
solution_elem_color = (178, 34, 34)
block_lines_color = (119,136,153)
grid_lines_color = (0, 0, 0)
buffer = 5

grid = np.zeros((9,9))

pygame.init()
window = pygame.display.set_mode(board_dims)
        
def insert(window, pos, font):
    i, j = pos[1], pos[0]
    pygame.draw.rect(window, block_lines_color, (pos[0]*50 + buffer, pos[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN:
                #if zero was pressed 
                if event.key == 48:
                    grid[i-1][j-1] = 0
                    pygame.draw.rect(window, background_color, (pos[0]*50 + buffer, pos[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                    return
                if (0 < event.key - 48 < 10):
                    pygame.draw.rect(window, background_color, (pos[0]*50 + buffer, pos[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    value = event.key-48
                    char = font.render(str(value), True, user_elem_color)
                    window.blit(char, (pos[0]*50 + 15, pos[1]*50 + 5))
                    grid[i-1][j-1] = value
                    pygame.display.update()
                    return

def display_error_text(window, pos):
    font = pygame.font.SysFont('lucidagrande', 15)
    error_text = 'Puzzle does not contain a solution :('
    text = font.render(error_text, True, solution_elem_color)
    window.blit(text, pos)
    pygame.display.update()

def solve():
    font = pygame.font.SysFont('lucidagrande', 35)
    try:
        ans = solve_sudoku(grid, method=3)
    except Exception as e:
        return False

    new_elems = ans - grid 
    filled_coords = np.argwhere(new_elems > 0)
    for coord in filled_coords:
        #draw the new vals onto the board 
        y,x = coord
        value = int(ans[y,x])
        win_y, win_x = int((y+1)*50 + 5), int((x+1)*50 + 15)
        char = font.render(str(value), True, solution_elem_color)
        window.blit(char, (win_x, win_y))
    pygame.display.update()
    return True

def main():
    #creating window 
    font = pygame.font.SysFont('lucidagrande', 35)
    pygame.display.set_caption("Sudoku Solver")
    window.fill(background_color)

    solve_img = pygame.image.load('solve_btn.png').convert_alpha()
    solve_button = Button((150, 510), solve_img, scale=0.5)

    #defining sudoku grid
    for i in range(10):
        #draw block lines
        pygame.draw.line(window, grid_lines_color, (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(window, grid_lines_color, (50, 50 + 50*i), (500, 50 + 50*i), 2)
        if i%3 == 0:
            pygame.draw.line(window, block_lines_color, (50 + 50*i, 50), (50+50*i, 500), 4)
            pygame.draw.line(window, block_lines_color, (50, 50+50*i), (500, 50+50*i), 4)

    pygame.display.update()

    run = True
    solved = False
    while run:
        if solve_button.draw(window):
            solved = solve()
            if not solved:
                display_error_text(window, (150, 25))
            else:
                #cover error text
                pygame.draw.rect(window, background_color, (150, 25, 300, 20))

        if solved == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 50 <= pos[0] <= 500 and 50 <= pos[1] <= 500:
                        insert(window, (pos[0]//50, pos[1]//50), font)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    
if __name__ == '__main__':
    main()