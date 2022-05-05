import typing
import evdev
from math import ceil

import lcdui
import charlcd


class CalcUI(lcdui.LcdUI):

    def __init__(self, lcd: charlcd.CharLcd):
        super().__init__(lcd)

        self.active_field = "entry_field"

        self.fields["entry_field"] = lcdui.TextField(
            (0, 0), self.lcd, length=20)
        self.fields["result_field"] = lcdui.TextField(
            (1, 0), self.lcd, length=20, rows=2, text=ProgCalcController.error_string)
        # self.fields["from_label"] = lcdui.TextField(
        #     (2, 0), self.lcd, text="from:")
        # self.fields["to_label"] = lcdui.TextField(
        #     (2, self.fields["from_label"].last_col + 2), self.lcd, text="to:")
        self.fields["from_field"] = lcdui.TextField(
            (3, 0), self.lcd, text="DEC")
        self.fields["to_field"] = lcdui.TextField(
            (3, 6), self.lcd, text="HEX")
        self.fields["arrow_field"] = lcdui.TextField(
            (3, 4), self.lcd, text="\x7e")

        self.lcd.set_backlight(True)
        self.lcd.set_cursor(False)
        self.lcd.set_blink(False)
        self.draw()
        self.lcd.set_position(*self.fields[self.active_field].coords)

    def select_field(self, field_name):
        self.active_field = field_name
        self.lcd.set_position(*self.fields[self.active_field].coords)


class ProgCalcController():

    character_keymap = {
        2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0',
        30: 'a', 48: 'b', 46: 'c', 32: 'd', 18: 'e', 33: 'f'
    }

    error_string = "??"

    formats = ["DEC", "HEX", "BIN"]

    def __init__(self, lcd: charlcd.CharLcd, input_device: evdev.InputDevice):
        self.lcd = lcd
        self.ui = CalcUI(self.lcd)
        self.input_device = input_device
        self.from_idx = 0
        self.to_idx = 1

    def handle_input(self):
        self.input_device.grab()

        key_event_generator = (evdev.KeyEvent(
            event) for event in self.input_device.read_loop() if event.type == evdev.ecodes.EV_KEY)

        for event in key_event_generator:
            if event.keystate == evdev.KeyEvent.key_down or event.keystate == evdev.KeyEvent.key_hold:
                character = ProgCalcController.character_keymap.get(
                    event.scancode)
                if character:
                    self.ui.fields["entry_field"].putchar(character.upper())

                elif event.keycode == 'KEY_BACKSPACE':
                    self.ui.fields["entry_field"].backspace()

                elif event.keycode == 'KEY_DELETE':
                    # clear input
                    self.ui.fields["entry_field"].clear()

                elif event.keycode == 'KEY_F1':
                    # cycle through from formats
                    self.from_idx = self.cycle_format(self.from_idx)
                    self.update_to_from()

                elif event.keycode == 'KEY_F2':
                    # swap from and to
                    temp = self.from_idx
                    self.from_idx = self.to_idx
                    self.to_idx = temp
                    self.update_to_from()


                elif event.keycode == 'KEY_F3':
                    # cycle through to formats
                    self.to_idx = self.cycle_format(self.to_idx)
                    self.update_to_from()

                self.do_conversion()

    def cycle_format(self, format_field):
        format_field += 1
        format_field %= len(ProgCalcController.formats)
        return format_field

    def update_to_from(self):
        self.ui.fields["from_field"].set_text(
            ProgCalcController.formats[self.from_idx])
        self.ui.fields["from_field"].draw()
        self.ui.fields["to_field"].set_text(
            ProgCalcController.formats[self.to_idx])
        self.ui.fields["to_field"].draw()

    def do_conversion(self):
        # get the current contents of the entry field
        from_val = self.ui.fields["entry_field"].raw_text
        intermediate = None
        result = None
        # look at from_type and to_type
        from_type = ProgCalcController.formats[self.from_idx]
        to_type = ProgCalcController.formats[self.to_idx]
        # convert from from_type to intermediary decimal
        try:

            if from_type == "DEC":
                intermediate = int(from_val)
            elif from_type == "HEX":
                intermediate = int(str(from_val), base=16)
            elif from_type == "BIN":
                intermediate = int(str(from_val), base=2)

            # convert from decimal to to_type
            if to_type == "DEC":
                result = str(intermediate)
            elif to_type == "HEX":
                result = hex(intermediate).upper()
            elif to_type == "BIN":
                raw_binary = bin(intermediate).lstrip("0b")
                num_nibbles = ceil(len(raw_binary) / 4)
                num_zeros = (num_nibbles * 4) - len(raw_binary)
                # zero pad to nearest nibble
                padded_binary = "0" * num_zeros + raw_binary
                nibbles = [padded_binary[i:i+4] for i in range(0, len(padded_binary) , 4)]
                result = " ".join(nibbles)

        # catch exceptions and set result field to some error message, maybe just "?"
        except:
            result = ProgCalcController.error_string

        self.ui.fields["result_field"].set_text(result)
        self.ui.fields["result_field"].draw()

        pass


if __name__ == "__main__":
    try:
        lcd = charlcd.CharLcd("/sys/class/alphalcd/lcdi2c", "/dev/lcdi2c")
        ctrl = ProgCalcController(lcd, evdev.InputDevice("/dev/input/event0"))
        ctrl.handle_input()
    except:
        lcd.set_backlight(False)
        lcd.clear()
