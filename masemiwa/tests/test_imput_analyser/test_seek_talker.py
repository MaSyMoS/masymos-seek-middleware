import unittest
from unittest.mock import patch

import pytest

import masemiwa.input_analyser.seek_talker as t


class TestSeekUrlObject(unittest.TestCase):
    def test_success(self):
        obj = t.SeekUrl('https://fairdomhub.org/models/24.json?version=3')
        self.assertEqual('https://fairdomhub.org/models/24', obj.url)
        self.assertEqual(24, obj.id)

    def test_inkscape(self):
        with pytest.raises(t.SeekUrlException):
            t.SeekUrl('inkscape.org')

    def test_incomplete(self):
        with pytest.raises(t.SeekUrlException):
            t.SeekUrl('https://fairdomhub.org/models/')

    def test_readonly_attributes(self):
        obj = t.SeekUrl('https://fairdomhub.org/models/24.json?version=3')
        with pytest.raises(AttributeError):
            obj.id = 42
        with pytest.raises(AttributeError):
            obj.url = "blablubb"


class TestJsonForResource(unittest.TestCase):
    """
    FIXME this test case should use a mock/monkey patch
    """

    def test_success(self):
        # t.logging.basicConfig(level=t.logging.DEBUG)
        self.assertIsNotNone(t.json_for_resource(t.SeekUrl("https://fairdomhub.org/models/24.json?version=3")))

    def test_403(self):
        self.assertIsNone(t.json_for_resource(t.SeekUrl("https://fairdomhub.org/models/22.json?version=3")))


if __name__ == '__main__':
    unittest.main()
