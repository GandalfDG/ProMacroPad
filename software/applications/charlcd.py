
import os

from base_ui import TextDevice


class CharLcd(TextDevice):

    RESET_FILE = "reset"
    BACKLIGHT_FILE = "brightness"
    DATA_FILE = "data"
    CURSOR_FILE = "cursor"
    BLINK_FILE = "blink"
    POS_FILE = "position"
    CLEAR_FILE = "clear"
    DEV_FILE = ""

    def __init__(self, sys_path, dev_path):
        super().__init__()
        self.sys_path = sys_path
        self.dev_path = dev_path

    def setup(self):
        self.set_backlight(True)
        self.set_cursor(False)
        self.set_blink(False)

    def teardown(self):
        lcd.set_backlight(False)
        lcd.clear()

    def set_blink(self, enable: bool):
        data = "1" if enable else "0"
        self._sys_file_write(data, CharLcd.BLINK_FILE)

    def set_backlight(self, enable: bool):
        data = "1" if enable else "0"
        self._sys_file_write(data, CharLcd.BACKLIGHT_FILE)

    def clear(self):
        self._sys_file_write("1", CharLcd.CLEAR_FILE, "w")

    def reset(self):
        self._sys_file_write("1", CharLcd.RESET_FILE, "w")

    def set_cursor(self, enable: bool):
        data = "1" if enable else "0"
        self._sys_file_write(data, CharLcd.CURSOR_FILE, "w")

    def set_position(self, row: int, col: int):
        data = bytearray([col, row])
        self._sys_file_write(data, CharLcd.POS_FILE, "wb")

    def write(self, data: str):
        with open(self.dev_path, "w") as devfile:
            devfile.write(data)

    def write_data(self, data: str):
        self._sys_file_write(data, CharLcd.DATA_FILE, "w")

    def append_data(self, data: str):
        self._sys_file_write(data, CharLcd.DATA_FILE, "a")

    def _sys_file_write(self, data: str, filename: str, mode="w"):
        with open(os.path.join(self.sys_path, filename), mode) as sys_file:
            sys_file.write(data)

    def _dev_file_write(self, data, filename: str, mode="w"):
        with open(os.path.join(self.dev_path, filename), mode) as dev_file:
            dev_file.write(data)


if __name__ == "__main__":
    lcd = CharLcd("/sys/class/alphalcd/lcdi2c", "/dev/lcdi2c")
