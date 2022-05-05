import typing

from charlcd import CharLcd
from base_ui import CoordType, TextField, TextUI

# LCD functions

# def draw(self):
#     for row in range(self.rows):
#         self.lcd.set_position(self.coords[0] + row, self.coords[1])
#         self.lcd.write(self.padded_text[self.length * row:(self.length * row) + self.length])

# def putchar(self, char):
#     newtext = self.text + str(char)
#     self.set_text(self.text + char)
#     self.draw()

# def backspace(self):
#     self.set_text(self.text[:-1])
#     self.draw()

# def clear(self):
#     self.set_text("")
#     self.draw()

# @property
# def end_coords(self):
#     return (self.coords[0], self.coords[1] + self.length - 1)

# @property
# def last_col(self):
#     return self.coords[1] + self.length - 1

class LcdUI(TextUI):
    def __init__(self, lcd_device: CharLcd):
        super().__init__(lcd_device)
        self.lcd = lcd_device
        self.lcd.reset()

    def draw_field(self, field: TextField):
        for row, line in enumerate(field.windowed_text)
            self.lcd.set_position(field.coords[0] + row, field.coords[1])
            self.lcd.write(line)


if __name__ == "__main__":
    lcd = CharLcd("/sys/class/alphalcd/lcdi2c", "/dev/lcdi2c")
    ui = LcdUI(lcd)
