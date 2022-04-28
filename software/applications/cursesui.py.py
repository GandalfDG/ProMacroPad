import curses

from base_ui import TextField, TextUI


class CursesUI(TextUI):
    def __init__(self, display_device, rows, cols):
        super().__init__(display_device, rows, cols)
        self.stdscr = curses.initscr()
        self.stdscr.noecho()
        self.stdscr.cbreak()

        self.window = curses.newwin(rows, cols)

    def add_field(self, field_name, field):
        super().add_field(field_name, field)

    def draw_field(self, field: TextField):
        self.window.addnstr(field.padded_text, field.cols)