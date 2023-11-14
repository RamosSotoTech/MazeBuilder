from tkinter import Tk, BOTH, Canvas

class Point():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y


class Line():
    def __init__(self, point1 : Point, point2 : Point) -> None:
        self.__point1 = point1
        self.__point2 = point2

    def draw(self, canvas : Canvas, fill_color="black"):
        canvas.create_line(self.__point1.x, self.__point1.y, self.__point2.x, 
                           self.__point2.y, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)


class Window():
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color):
        line.draw(self.__canvas, fill_color=fill_color)   


def main():
    pass

if __name__ == "__main__":
    pass