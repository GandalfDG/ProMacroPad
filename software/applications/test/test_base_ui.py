import unittest
from ..base_ui import ScrollableTextField, TextField


class TestTextField(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.test_str = "hello"

    def test_assumptions(self):
        field1 = TextField((0, 0), self.test_str)

        self.assertEqual(field1.cols, len(self.test_str))
        self.assertEqual(field1.rows, 1)
        self.assertEqual(field1.text, self.test_str)
        self.assertEqual(field1.padded_text, self.test_str)
        self.assertEqual(field1.wrapped_text[0], self.test_str)

    def test_padding(self):
        field_len = 10
        field = TextField((0, 0), self.test_str, field_len)

        self.assertEqual(len(field.padded_text), field.cols)
        self.assertEqual(field.padded_text, self.test_str +
                         ' ' * (field_len - len(self.test_str)))

    def test_truncate(self):
        field = TextField((0,0), self.test_str, 3)

        self.assertEqual(field.padded_text, self.test_str[:3])

    def test_multiline(self):
        field_cols = 10
        field_rows = 2
        field = TextField((0,0), self.test_str, field_cols, field_rows)

        field.set_text("*" * (field.cols * field.rows - 5))

        self.assertEqual(len(field.wrapped_text), field.rows)
        self.assertEqual(field.wrapped_text[1], "*" * (field_cols - 5) + ' ' * (field_cols - (field_cols - 5)))

class TestScrollableTextField(unittest.TestCase):

    def setUp(self) -> None:
        self.field1 = ScrollableTextField((0,0), "123456", 3, 1)
        self.field2 = ScrollableTextField((0,0), "123456789", 3, 2)
        return super().setUp()

    def test_wrapping(self):
        self.assertEqual(len(self.field1.full_lines), 2)
        self.assertEqual(len(self.field1.wrapped_text), 1)

        self.assertEqual(len(self.field2.full_lines), 3)
        self.assertEqual(len(self.field2.wrapped_text), 2)

    def test_scrolling(self):
        self.field1.scroll_to(1)
        self.assertEqual("456", self.field1.wrapped_text[0])
        self.assertRaises(ValueError, self.field1.scroll_to, 10)
        self.assertRaises(ValueError, self.field1.scroll_to, 2)
        self.assertRaises(ValueError, self.field1.scroll_to, -1)
