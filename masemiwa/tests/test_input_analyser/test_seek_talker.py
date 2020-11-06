import unittest
from unittest.mock import patch

import pytest

import masemiwa.input_analyser.beans
import masemiwa.input_analyser.seek_talker as t
from masemiwa.input_analyser import InputAnalyseErrorReason, InputAnalyseError


class TestSeekUrlObject(unittest.TestCase):
    def test_success(self):
        obj = masemiwa.input_analyser.beans.SeekUrl('https://fairdomhub.org/models/24.json?version=3')
        self.assertEqual('https://fairdomhub.org/models/24', obj.url)
        self.assertEqual(24, obj.id)

    def test_inkscape(self):
        with pytest.raises(InputAnalyseError) as e:
            masemiwa.input_analyser.beans.SeekUrl('inkscape.org')
        self.assertEqual(InputAnalyseErrorReason.URL_INVALID,e.value.reason)

    def test_incomplete(self):
        with pytest.raises(InputAnalyseError) as e:
            masemiwa.input_analyser.beans.SeekUrl('https://fairdomhub.org/models/')
        self.assertEqual(InputAnalyseErrorReason.URL_INVALID,e.value.reason)

    def test_readonly_attributes(self):
        obj = masemiwa.input_analyser.beans.SeekUrl('https://fairdomhub.org/models/24.json?version=3')
        with pytest.raises(AttributeError):
            obj.id = 42
        with pytest.raises(AttributeError):
            obj.url = "blablubb"


class TestDownloadSeekMetadata(unittest.TestCase):
    """
    FIXME this test case should use a mock/monkey patch
    """

#    def test_success(self):
#        # t.logging.basicConfig(level=t.logging.DEBUG)
#        self.assertIsNotNone(t.download_seek_metadata(t.SeekUrl("https://fairdomhub.org/models/24.json?version=3")))
#
#    def test_403(self):
#        self.assertIsNone(t.download_seek_metadata(t.SeekUrl("https://fairdomhub.org/models/22.json?version=3")))


if __name__ == '__main__':
    unittest.main()
