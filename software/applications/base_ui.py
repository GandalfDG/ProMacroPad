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

    def __init__(self, coords: CoordType, text="", cols=None, rows=None):
        self.coords: CoordType = coords
        self.cols: int = cols if cols else len(text)
        self.rows: int = rows if rows else 1
        self.text: str = text
        self.padded_text: str = ""
        self.wrapped_text: typing.List[str] = []
        self.set_text(self.text)

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
        self.text = truncated
        # pad with spaces to field length
        padded = truncated + (" " * ((self.cols * self.rows) - len(truncated)))
        self.padded_text = padded

        self.wrapped_text = []
        for row in range(self.rows):
            self.wrapped_text.append(
                self.padded_text[self.cols * row:(self.cols * row) + self.cols])


class ScrollableTextField(TextField):
    """
    TODO
    A text field which may contain more than rows*cols characters, allowing
    vertical scrolling
    """
    def __init__(self, coords: CoordType, text="", cols=None, rows=None):
        super().__init__(coords, text, cols, rows)

    def set_text(self, text: str):
        return super().set_text(text)


class TextUI(ABC):

    def __init__(self, display_device: typing.Any, rows=4, cols=20):
        """
        Initialize any state needed by the display device
        """
        self.fields: typing.Dict[str, TextField] = {}
        self._sorted_fields: typing.List[TextField] = []
        self.device = display_device
        self.dimensions = (rows, cols)

    def add_field(self, field_name: str, field: TextField):
        self.fields[field_name] = field
        self._sorted_fields = sorted(self.fields.values())

    def redraw(self):
        for field in self._sorted_fields:
            self.draw_field(field)

    @abstractmethod
    def draw_field(self, field: TextField):
        pass
