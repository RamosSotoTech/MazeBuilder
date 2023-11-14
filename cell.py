from graphics import Line, Point, Window


class Cell():
    TOP = 0b0001
    RIGHT = 0b0010
    BOTTOM = 0b0100
    LEFT = 0b1000
    ALL = 0b1111

    def __init__(self, window:Window) -> None:
        self.corners = self.ALL
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.lines = {self.TOP: None, self.RIGHT: None, self.BOTTOM: None, self.LEFT: None}
        self.win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

        black_or_white = (lambda corner: "black" if self.corners & corner else "white")
        
        self.lines[Cell.TOP] = Line(Point(x=self.x1, y=self.y1), Point(x=self.x2, y=self.y1))
        self.lines[Cell.RIGHT] = Line(Point(x=self.x2, y=self.y1), Point(x=self.x2, y=self.y2))
        self.lines[Cell.BOTTOM] = Line(Point(x=self.x1, y=self.y2), Point(x=self.x2, y=self.y2))
        self.lines[Cell.LEFT] = Line(Point(x=self.x1, y=self.y1), Point(x=self.x1, y=self.y2))
        self.win.draw_line(self.lines[Cell.TOP], black_or_white(Cell.TOP))
        self.win.draw_line(self.lines[Cell.RIGHT], black_or_white(Cell.RIGHT))
        self.win.draw_line(self.lines[Cell.BOTTOM], black_or_white(Cell.BOTTOM))
        self.win.draw_line(self.lines[Cell.LEFT], black_or_white(Cell.LEFT))

    def draw_move(self, to_cell, undo=False):
        from_center_x = (self.x1 + self.x2)/2
        from_center_y = (self.y1 + self.y2)/2
        to_center_x = (to_cell.x1 + to_cell.x2)/2
        to_center_y = (to_cell.y1 + to_cell.y2)/2
        color = "black" if undo else "red"
        line = Line(Point(from_center_x, from_center_y), Point(to_center_x, to_center_y))
        self.win.draw_line(line, color)
