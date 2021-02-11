import pygame
from globals import *
from ui.components import Grid

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku-Solver")
GRID = Grid()
NUM_MAP = [eval(f"pygame.K_{i}") for i in range(0, 10)] + [eval(f"pygame.K_KP{i}") for i in range(0, 10)]


def example():
    example_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    for i in range(9):
        for j in range(9):
            GRID.grid[i][j].val = example_board[i][j]


example()


def redraw_win():
    win.fill(white)
    GRID.draw(win)
    pygame.display.flip()


def main():
    RUN = True
    while RUN:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                r, c = GRID.get_row_col_clicked(event.pos)
                GRID.select(r, c)
            elif event.type == pygame.KEYDOWN:
                if event.key in NUM_MAP and GRID.selected:
                    key = NUM_MAP.index(event.key)
                    num = key if key <= 9 else key - 10
                    rs, cs = GRID.selected
                    if num and GRID.is_valid(num):
                        GRID.grid[rs][cs].val = num
                    else:
                        GRID.grid[rs][cs].val = None
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    GRID.solve()
                elif event.key == pygame.K_r:
                    GRID.reset()
        redraw_win()
    pygame.quit()


if __name__ == "__main__":
    main()
