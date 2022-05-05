"""
This module contains base classes used for representing UI elements on a text display
"""

import typing
from abc import ABC, abstractmethod

CoordType = typing.Tuple[int, int]


class TextField():
    """
    A TextField object represents a rectangular area of a display which may contain text.
    The text field maintains the text content, as well as the location and dimensions of
    the area.
    """

    def __init__(self, coords: CoordType, text: str = "", cols: int = None, rows: int = None):
        self.coords: CoordType = coords
        self.cols: int = cols if cols else len(text)
        self.rows: int = rows if rows else 1
        self.raw_text: str = text
        self.padded_text: str = ""
        self.windowed_text: typing.List[str] = []
        self.set_text(self.raw_text)

    def __lt__(self, other):
        if self.coords[0] == other.coords[0]:
            return True if self.coords[1] < other.coords[1] else False
        else:
            return True if self.coords[0] < other.coords[0] else False

    def set_text(self, text: str):
        """
        Set the text contained by the field. The text will be truncated to fit the field's length.
        TODO for multi-row fields handle wrapping
        """
        truncated = text[:self.cols *
                         self.rows]  # truncate to the length of the field
        self.raw_text = truncated
        # pad with spaces to field length
        padded = truncated + (" " * ((self.cols * self.rows) - len(truncated)))
        self.padded_text = padded

        self.windowed_text = []
        for row in range(self.rows):
            self.windowed_text.append(
                self.padded_text[self.cols * row:(self.cols * row) + self.cols])


class ScrollableTextField(TextField):
    """
    TODO
    A text field which may contain more than rows*cols characters, allowing
    vertical scrolling
    """

    def __init__(self, coords: CoordType, text="", cols=None, rows=None):
        self.top_row = 0
        self.full_lines = [1, 2]
        super().__init__(coords, text, cols, rows)

    def set_text(self, text: str):
        self.raw_text = text
        self.full_lines = [self.raw_text[i*self.cols:i*self.cols+self.cols]
                           for i in range(int(len(self.raw_text)/self.cols))]
        self.windowed_text = self.full_lines[self.top_row:self.top_row+self.rows]

    def scroll_to(self, row):
        if row > self.max_scroll or row < 0:
            raise ValueError(
                f"scrolled too far, max scroll row = {self.max_scroll}")
        self.top_row = row
        self.set_text(self.raw_text)

    @property
    def max_scroll(self) -> int:
        return len(self.full_lines) - self.rows

    @property
    def scrolled_percentage(self) -> float:
        return self.top_row / self.max_scroll


class TextDevice(ABC):
    """
    any text device should be able to do at least a subset of what CharLcd does
    e.g. clear, set cursor position, write data, etc.
    """
    @abstractmethod
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def teardown(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def set_position(self, row: int, col: int):
        pass

    @abstractmethod
    def write(self, data: str):
        pass


class TextUI(ABC):

    def __init__(self, display_device: TextDevice):
        """
        Initialize any state needed by the display device
        """
        self.fields: typing.Dict[str, TextField] = {}
        self._sorted_fields: typing.List[TextField] = []
        self.device = display_device
        self.device.setup()

    def setup(self):
        self.device.setup()

    def teardown(self):
        self.device.teardown()

    def add_field(self, field_name: str, field: TextField):
        self.fields[field_name] = field
        self._sorted_fields = sorted(self.fields.values())

    def redraw(self):
        for field in self._sorted_fields:
            self.draw_field(field)

    @abstractmethod
    def draw_field(self, field: TextField):
        pass
