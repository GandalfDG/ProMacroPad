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


if __name__ == "__main__":
    unittest.main()
