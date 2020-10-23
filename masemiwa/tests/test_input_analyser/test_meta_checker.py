import unittest

import masemiwa.input_analyser.meta_checker as t


class TestMime(unittest.TestCase):
    def test_string(self):
        self.assertFalse(t._check_mime_type('wrong'))

    def test_number(self):
        self.assertFalse(t._check_mime_type(42))

    def test_wrong_mime(self):
        self.assertFalse(t._check_mime_type('text/plain'))

    def test_right_mime(self):
        self.assertTrue(t._check_mime_type('application/xml'))


if __name__ == '__main__':
    unittest.main()
