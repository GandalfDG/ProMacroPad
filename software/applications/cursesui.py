import curses
from os import device_encoding

from base_ui import TextDevice, TextField, TextUI
import progcalc

class CursesDevice(TextDevice):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def teardown(self):
        pass

    def clear(self):
        return super().clear()

    def set_position(self, row: int, col: int):
        return super().set_position(row, col)

    def write(self, data: str):
        return super().write(data)

class CursesUI(TextUI):
    def __init__(self, display_device, rows, cols):
        super().__init__(display_device, rows, cols)
        
        self.window = curses.newwin(rows, cols, 1, 1)
        self.window.border()

    def add_field(self, field_name, field):
        super().add_field(field_name, field)


    def redraw(self):
        super().redraw()
        self.window.refresh()

    def draw_field(self, field: TextField):
        for row, line in enumerate(field.windowed_text):
            self.window.addnstr(field.coords[0] + row, field.coords[1], line, field.cols)

def main(scr):
    device = CursesDevice()
    progcalc.CalcUI(device)


if __name__ == "__main__":
    import random
    curses.wrapper(main)
    