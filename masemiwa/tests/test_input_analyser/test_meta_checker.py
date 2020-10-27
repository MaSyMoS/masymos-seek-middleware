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


class Test(TestCase):
    def test_check_content_blob(self):
        # TODO mock _download_blob_content()
        self.fail()

    def test__download_blob_content(self):
        # TODO mock downloading
        self.fail()

    namespace_valid1: str = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Created by Schorsch on 2011/04/04 15:53:02-->
<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">
<model name="Schorsch" >
</model></sbml>
"""

    def test__check_namespace(self):
        self.assertTrue(t._check_namespace(self.namespace_valid1))
