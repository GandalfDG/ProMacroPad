import typing

from charlcd import CharLcd
from base_ui import CoordType, TextField, TextUI



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
