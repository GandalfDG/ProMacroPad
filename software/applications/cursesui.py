import curses
import evdev
from os import device_encoding

from base_ui import TextDevice, TextField, TextUI
import progcalc


class CursesDevice(TextDevice):


    def setup(self):
        main_window = curses.newwin(self.rows + 2, self.cols + 2, 0, 0)
        main_window.border()
        self.window = curses.newwin(self.rows, self.cols, 1, 1)
        return super().setup()

    def teardown(self):
        pass

    def clear(self):
        return super().clear()

    def set_position(self, row: int, col: int):
        return super().set_position(row, col)

    def write(self, data: str):
        return super().write(data)


class CursesUI(TextUI):
    def __init__(self, display_device):
        super().__init__(display_device)

    def redraw(self):
        super().redraw()
        self.window.refresh()

    def draw_field(self, field: TextField):
        for row, line in enumerate(field.windowed_text):
            self.window.addnstr(
                field.coords[0] + row, field.coords[1], line, field.cols)


def main(scr):
    dev = CursesDevice(4, 20)
    progcalc.CalcUI()
    ctrl = progcalc.ProgCalcController(
        dev, evdev.InputDevice("/dev/input/event0"))
    ctrl.handle_input()


if __name__ == "__main__":
    import random
    curses.wrapper(main)
