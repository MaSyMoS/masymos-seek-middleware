import unittest

import masemiwa.input_analyser.beans as b
import masemiwa.input_analyser.seek_talker as t


class TestDownloadSeekMetadata(unittest.TestCase):
    """
    FIXME this test case should use a mock/monkey patch
    """

    # def test_success(self):
    #     # t.logging.basicConfig(level=t.logging.DEBUG)
    #     self.assertIsNotNone(t.download_seek_metadata(b.SeekUrl("https://fairdomhub.org/models/24.json?version=3")))
    #
    # def test_403(self):
    #     self.assertIsNone(t.download_seek_metadata(b.SeekUrl("https://fairdomhub.org/models/22.json?version=3")))


class TestDownloadSeekContentBlobData(unittest.TestCase):
    """
    FIXME this test case should use a mock/monkey patch
    """

    # def test_success(self):
    #     self.assertIsNotNone(
    #         t._download_blob_content(b.SeekContentBlob({'link': 'https://fairdomhub.org/models/24/content_blobs/115'})))
    #
    # def test_403(self):
    #     self.assertIsNone(
    #         t._download_blob_content(b.SeekContentBlob({'link': 'https://fairdomhub.org/models/22/content_blobs/115'})))


if __name__ == '__main__':
    unittest.main()
