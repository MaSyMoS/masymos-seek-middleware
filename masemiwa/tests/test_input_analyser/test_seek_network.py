import unittest

import responses
from requests import HTTPError
from urllib3.exceptions import ConnectTimeoutError

import masemiwa.input_analyser.beans as b
import masemiwa.input_analyser.seek_network as t


class TestDownloadSeekMetadata(unittest.TestCase):
    @responses.activate
    def test_mock_200(self):
        responses.add(responses.GET, 'https://my-url.org/models/42.json',
                      json={'some': 'thing'}, status=200)

        # 200
        self.assertEqual("thing",
                         t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/42")).get(
                             'some'))
        self.assertEqual("thing",
                         t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/42.json")).get(
                             'some'))
        self.assertEqual("thing",
                         t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/42.json?version=3")).get(
                             'some'))

    @responses.activate
    def test_mock_400(self):
        responses.add(responses.GET, 'https://my-url.org/models/52.json',
                      status=403)
        responses.add(responses.GET, 'https://my-url.org/models/62.json',
                      status=404)

        # 403, 404
        self.assertIsNone(t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/52")))
        self.assertIsNone(t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/62")))

    @responses.activate
    def test_mock_error(self):
        responses.add(responses.GET, 'https://my-url.org/models/142.json',
                      status=200, body=ConnectTimeoutError())
        responses.add(responses.GET, 'https://my-url.org/models/143.json',
                      status=200, body=HTTPError())

        # error handling
        self.assertIsNone(t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/142")))
        self.assertIsNone(t.download_seek_metadata(b.SeekUrl("https://my-url.org/models/143")))


class TestDownloadSeekContentBlobData(unittest.TestCase):
    @responses.activate
    def test_mock_200(self):
        responses.add(responses.GET, 'https://my-url.org/models/42/content_blobs/123/download',
                      body="<xml1 />", status=200)
        responses.add(responses.GET, 'https://my-url.org/models/52/content_blobs/124/download',
                      body="<xml2 />", status=200)

        # 200
        self.assertEqual("<xml1 />",
                         t.download_blob_content(b.SeekContentBlob(
                             {'content_type': 'blo', 'link': 'https://my-url.org/models/42/content_blobs/123'})))
        self.assertEqual("<xml2 />",
                         t.download_blob_content(b.SeekContentBlob(
                             {'content_type': 'blo', 'link': 'https://my-url.org/models/52/content_blobs/124'})))

    @responses.activate
    def test_mock_400(self):
        responses.add(responses.GET, 'https://my-url.org/models/62/content_blobs/125/download',
                      status=403)
        responses.add(responses.GET, 'https://my-url.org/models/72/content_blobs/126/download',
                      status=404)

        # 403, 404
        self.assertIsNone(t.download_blob_content(b.SeekContentBlob(
            {'content_type': 'blo', 'link': 'https://my-url.org/models/62/content_blobs/125'})))
        self.assertIsNone(t.download_blob_content(b.SeekContentBlob(
            {'content_type': 'blo', 'link': 'https://my-url.org/models/72/content_blobs/126'})))

    @responses.activate
    def test_mock_error(self):
        responses.add(responses.GET, 'https://my-url.org/models/62/content_blobs/125/download',
                      status=200, body=ConnectTimeoutError())
        responses.add(responses.GET, 'https://my-url.org/models/72/content_blobs/126/download',
                      status=200, body=HTTPError())

        # 403, 404
        self.assertIsNone(t.download_blob_content(b.SeekContentBlob(
            {'content_type': 'blo', 'link': 'https://my-url.org/models/62/content_blobs/125'})))
        self.assertIsNone(t.download_blob_content(b.SeekContentBlob(
            {'content_type': 'blo', 'link': 'https://my-url.org/models/72/content_blobs/126'})))


if __name__ == '__main__':
    unittest.main()
