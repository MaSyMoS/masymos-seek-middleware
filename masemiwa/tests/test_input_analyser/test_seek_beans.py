from unittest import TestCase

import masemiwa.input_analyser.seek_beans as t


class TestContentBlob(TestCase):
    def test_success(self):
        self.assertEqual('blo', t.ContentBlob({'content_type': 'blo'}).mime)
        self.assertEqual('bla', t.ContentBlob({'link': 'bla'}).link)
        cb = t.ContentBlob({'content_type': 'blo', 'link': 'bla'})
        self.assertEqual('blo', cb.mime)
        self.assertEqual('bla', cb.link)


class TestSeekJson(TestCase):
    def test_success(self):
        self.assertEqual('1234', t.SeekJson({'data': {'id': '1234'}}).id)
        self.assertEqual('5', t.SeekJson({'data': {'attributes': {'latest_version': '5'}}}).latest_version)
        self.assertEqual('hurra', t.SeekJson(
            {'data': {'attributes': {'content_blobs': {'0': {'link': 'hurra'}}}}}).content_blobs[0].link)

        s = t.SeekJson({'data': {'id': '1234',
                                 'attributes': {'latest_version': '5',
                                                'content_blobs': {'0': {'link': 'hurra'}}}}})
        self.assertEqual('1234', s.id)
        self.assertEqual('5', s.latest_version)
        self.assertEqual('hurra', s.content_blobs[0].link)
