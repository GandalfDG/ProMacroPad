import unittest
from ..base_ui import TextField


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
        return super().setUp()

