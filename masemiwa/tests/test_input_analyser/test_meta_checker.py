import unittest
from unittest import TestCase

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


class TestCheckContentBlob(TestCase):
    def test_check_content_blob(self):
        self.fail()


class Test(TestCase):
    def test__download_blob_content(self):
        self.fail()
