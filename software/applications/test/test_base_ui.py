import unittest

from sys import path as syspath
from os import path as ospath

path = ospath.abspath("../")

syspath.insert(1,path)

from ..base_ui import TextField

class TestTextField(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_assumptions(self):
        test_str = "hello"
        field1 = TextField((0,0), test_str)

        self.assertEqual(field1.cols, len(test_str))
        self.assertEqual(field1.rows, 1)
        self.assertEqual(field1.text, test_str)
        self.assertEqual(field1.padded_text, test_str)
        self.assertEqual(field1.wrapped_text[0], test_str)

if __name__=="__main__":
    unittest.main()