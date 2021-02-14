import pygame
from globals import *
pygame.font.init()
FONT = pygame.font.SysFont(None, 30)


class Grid:
    def __init__(self):
        self.dim = 9
        self.size = SCREEN_WIDTH // self.dim
        self.grid = self.init_grid()
        self.selected = None

    def init_grid(self):
        grid = [[] for _ in range(self.dim)]
        for r in range(self.dim):
            for c in range(self.dim):
                box = Box(self.size * c, self.size * r)
                grid[r].append(box)
        return grid

    def draw(self, win):
        for r in range(self.dim):
            for c in range(self.dim):
                self.grid[r][c].draw(win)
        for r in range(0, self.dim, 3):
            for c in range(0, self.dim, 3):
                pygame.draw.rect(win, blue, (self.size * c, self.size * r, box_size * 3, box_size * 3), 1)
        if self.selected:
            rs, cs = self.selected
            self.grid[rs][cs].draw(win)

    def select(self, r, c):
        if self.selected:
            rs, cs = self.selected
            self.grid[rs][cs].select()
        self.selected = (r, c)
        self.grid[r][c].select()

    def is_valid(self, val, pos=None):
        if pos is None:
            pos = self.selected
        rs, cs = pos
        for i in range(self.dim):
            if i != cs and self.grid[rs][i].val == val:
                return False
        for i in range(self.dim):
            if i != rs and self.grid[i][cs].val == val:
                return False
        r = rs // 3
        c = cs // 3
        for y in range(r * 3, r * 3 + 3):
            for x in range(c * 3, c * 3 + 3):
                if (y, x) != (rs, cs) and self.grid[y][x].val == val:
                    return False
        return True

    def get_row_col_clicked(self, pos):
        row = pos[1] // self.size
        col = pos[0] // self.size
        return row, col

    def find_empty(self):
        for r in range(self.dim):
            for c in range(self.dim):
                if not self.grid[r][c].val:
                    return r, c
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        rm, cm = empty
        for num in range(1, 10):
            if self.is_valid(num, empty):
                self.grid[rm][cm].val = num
                if self.solve():
                    return True
                self.grid[rm][cm].val = None
        return False

    def reset(self):
        self.__init__()


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, box_size, box_size)
        self.val = None
        self.selected = False

    def draw(self, win):
        color = red if self.selected else black
        pygame.draw.rect(win, color, self.rect, 1)
        if self.val:
            val = FONT.render(str(self.val), False, black)
            win.blit(val, val.get_rect(center=self.rect.center))

    def select(self):
        self.selected = False if self.selected else True
