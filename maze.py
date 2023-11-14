from typing import Any, Union
from graphics import Window, Point, Line
from cell import Cell
import time
import random

class Maze():
    def __init__(self, x1, y1, num_row, num_cols, cell_size_x, cell_size_y, win: Window | None = None, seed = None) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_row = num_row
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()
        if seed:
            random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        

    def _create_cells(self):
        self._cells = [[Cell(self.win) for _ in range(self.num_row)] for _ in range(self.num_cols)]
        for i in range(self.num_cols):
            for j in range(self.num_row):
                self._draw_cells(i, j)

    def _draw_cells(self, i, j):
        if self.win is None:
            return
        cell_x1 = self.x1 + j * self.cell_size_x
        cell_y1 = self.y1 + i * self.cell_size_y
        cell_x2 = cell_x1 + self.cell_size_x
        cell_y2 = cell_y1 + self.cell_size_y
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.04)

    def _break_entrance_and_exit(self):
        self._cells[0][0].corners = Cell.ALL ^ Cell.TOP
        self._draw_cells(0, 0)
        self._cells[-1][-1].corners = Cell.ALL ^ Cell.BOTTOM
        self._draw_cells(self.num_cols-1, self.num_row-1)

    def _break_walls_r(self, i, j):
        if self._cells[i][j].visited:
            return

        self._cells[i][j].visited = True

        directions = [(0, -1, Cell.LEFT), (0, 1, Cell.RIGHT), (-1, 0, Cell.TOP), (1, 0, Cell.BOTTOM)]
        opposite_wall = {Cell.LEFT: Cell.RIGHT, Cell.RIGHT: Cell.LEFT, Cell.TOP: Cell.BOTTOM, Cell.BOTTOM: Cell.TOP}

        random.shuffle(directions)

        for di, dj, wall in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_row and not self._cells[ni][nj].visited:
                self._cells[i][j].corners ^= wall
                self._cells[ni][nj].corners ^= opposite_wall[wall]

                self._break_walls_r(ni, nj)

        self._draw_cells(i, j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_row):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()

        self._cells[i][j].visited = True

        if i == self.num_cols - 1 and j == self.num_row - 1:
            return True

        directions = [(0, -1, Cell.LEFT), (0, 1, Cell.RIGHT), (-1, 0, Cell.TOP), (1, 0, Cell.BOTTOM)]

        for di, dj, wall in directions:
            ni, nj = i + di, j + dj

            if 0 <= ni < self.num_cols and 0 <= nj < self.num_row:
                if not self._cells[i][j].corners & wall and not self._cells[ni][nj].visited:
                    self._cells[i][j].draw_move(self._cells[ni][nj])

                    if self._solve_r(ni, nj):
                        return True

                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)
        return False

    def solve(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
        return self._solve_r(0, 0)
