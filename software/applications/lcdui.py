import typing

from charlcd import CharLcd

CoordType = typing.Tuple[int, int]


class TextField():
    def __init__(self, coords: CoordType, lcd: CharLcd, text="", length=None, rows=None):
        self.coords = coords
        self.length = length if length else len(text)
        self.rows = rows if rows else 1
        self.lcd = lcd
        self.text = text
        self.padded_text = text

    def __lt__(self, other):
        if self.coords[0] == other.coords[0]:
            return True if self.coords[1] < other.coords[1] else False
        else:
            return True if self.coords[0] < other.coords[0] else False

    def set_text(self, text: str):
        truncated = text[:self.length * self.rows]  # truncate to the length of the field
        self.text = truncated
        # pad with spaces to field length
        padded = truncated + (" " * ((self.length * self.rows) - len(truncated)))
        self.padded_text = padded

    def draw(self):
        for row in range(self.rows):
            self.lcd.set_position(self.coords[0] + row, self.coords[1])
            self.lcd.write(self.padded_text[self.length * row:(self.length * row) + self.length])

    def putchar(self, char):
        newtext = self.text + str(char)
        self.set_text(self.text + char)
        self.draw()

    def backspace(self):
        self.set_text(self.text[:-1])
        self.draw()
    
    def clear(self):
        self.set_text("")
        self.draw()

    @property
    def end_coords(self):
        return (self.coords[0], self.coords[1] + self.length - 1)

    @property
    def last_col(self):
        return self.coords[1] + self.length - 1

class LcdUI():
    def __init__(self, lcd: CharLcd):
        self.lcd = lcd
        self.lcd.reset()
        self.fields: typing.Dict[str, TextField] = {}

    def add_field(self, field_name: str, field: TextField):
        self.fields[field_name] = field

    def draw(self):
        for field in sorted(self.fields.values()):
            field.draw()


if __name__ == "__main__":
    lcd = CharLcd("/sys/class/alphalcd/lcdi2c", "/dev/lcdi2c")
    ui = LcdUI(lcd)
