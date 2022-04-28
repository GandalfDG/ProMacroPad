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
        self.coords = coords
        self.cols = cols if cols else len(text)
        self.rows = rows if rows else 1
        self.text = text
        self.padded_text = text

    def __lt__(self, other):
        if self.coords[0] == other.coords[0]:
            return True if self.coords[1] < other.coords[1] else False
        else:
            return True if self.coords[0] < other.coords[0] else False

    def set_text(self, text: str):
        """
        Set the text contained by the field. The text will be truncated to fit the field's length.
        """
        truncated = text[:self.cols * self.rows]  # truncate to the length of the field
        self.text = truncated
        # pad with spaces to field length
        padded = truncated + (" " * ((self.cols * self.rows) - len(truncated)))
        self.padded_text = padded

class TextUI(ABC):

    def __init__(self, display_device: typing.Any):
        """
        Initialize any state needed by the display device
        """
        self.fields: typing.Dict[str, TextField] = {} 
        self._sorted_fields: typing.list[TextField] = []

    def add_field(self, field_name: str, field: TextField):
        self.fields[field_name] = field
        self._sorted_fields = sorted(self.fields.values())

    def redraw(self):
        for field in self._sorted_fields:
            self.draw_field(field)

    @abstractmethod
    def draw_field(self, field: TextField):
        pass
        




    