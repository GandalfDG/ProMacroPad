# import unittest

# import charlcd
# import lcdui

# class TestTextField(unittest.TestCase):

#     def setUp(self) -> None:
#         super().setUp()
#         self.lcd = charlcd.CharLcd(None, None)

#     def test_sort(self):
#        field1 = lcdui.TextField((0,0), 5, self.lcd)
#        field2 = lcdui.TextField((0,1), 5, self.lcd)
#        field3 = lcdui.TextField((1,0), 5, self.lcd)
#        field4 = lcdui.TextField((1,1), 5, self.lcd)

#        field_list = [field4, field2, field3, field1]

#        sorted_list = sorted(field_list)

#        self.assertListEqual([field1, field2, field3, field4], sorted_list)

# if __name__ == "__main__":
#     unittest.main()