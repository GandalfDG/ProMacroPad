import curses

from base_ui import TextField, TextUI


class CursesUI(TextUI):
    def __init__(self, display_device, rows, cols):
        super().__init__(display_device, rows, cols)
        
        self.window = curses.newwin(rows, cols, 1, 1)

    def add_field(self, field_name, field):
        super().add_field(field_name, field)


    def redraw(self):
        super().redraw()
        self.window.refresh()

    def draw_field(self, field: TextField):
        self.window.addnstr(field.coords[0], field.coords[1], field.padded_text, field.cols + 1)

def main(scr):

    ui = CursesUI(None, 4, 20)
    curses.curs_set(0)
    ui.add_field("asdf", TextField((3, 2), "hello", 8, 1))
    ui.add_field("123", TextField((0, 0), "1"))

    while True:
        ui.fields["123"].set_text(str(random.randint(1, 10)))
        ui.redraw()
        pass


if __name__ == "__main__":
    import random
    curses.wrapper(main)
    