import unittest
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
            obj.id=42
        with pytest.raises(AttributeError):
            obj.url="blablubb"

if __name__ == '__main__':
    unittest.main()
