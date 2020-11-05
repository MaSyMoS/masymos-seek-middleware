from unittest import TestCase

import pytest

import masemiwa.input_analyser.beans as t


class TestSeekContentBlob(TestCase):
    def test_success(self):
        self.assertEqual('blo', t.SeekContentBlob({'content_type': 'blo'}).mime)
        self.assertEqual('bla', t.SeekContentBlob({'link': 'bla'}).link)
        cb = t.SeekContentBlob({'content_type': 'blo', 'link': 'bla'})
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


class TestXmlNamespace(TestCase):

    def test__extract_level_version_from_namespace(self):
        self.assertEqual(2, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/level2/version4")[0])
        self.assertEqual(4, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/level2/version4")[1])
        self.assertEqual(None, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/version4")[0])
        self.assertEqual(4, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/version4")[1])
        self.assertEqual(2, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/level2")[0])
        self.assertEqual(None, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/level2")[1])
        self.assertEqual(None, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/")[0])
        self.assertEqual(None, t._extract_level_version_from_namespace("http://www.sbml.org/sbml/")[0])

    def test_success(self):
        self.assertEqual("http://www.sbml.org/sbml/level2/version4",
                         t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2, version=4).namespace)
        self.assertEqual(2, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2, version=4).level)
        self.assertEqual(4, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2, version=4).version)

        self.assertEqual("http://www.sbml.org/sbml/level2/version4",
                         t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2).namespace)
        self.assertEqual(2, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2).level)
        self.assertEqual(4, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2).version)

        self.assertEqual("http://www.sbml.org/sbml/level2/version4",
                         t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", version=4).namespace)
        self.assertEqual(2, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", version=4).level)
        self.assertEqual(4, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", version=4).version)

        self.assertEqual("http://www.sbml.org/sbml/level2/version4",
                         t.XmlNamespace("http://www.sbml.org/sbml/level2/version4").namespace)
        self.assertEqual(2, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4").level)
        self.assertEqual(4, t.XmlNamespace("http://www.sbml.org/sbml/level2/version4").version)

        self.assertEqual("http://www.sbml.org/sbml/",
                         t.XmlNamespace("http://www.sbml.org/sbml/").namespace)
        self.assertIsNone(t.XmlNamespace("http://www.sbml.org/sbml/").level)
        self.assertIsNone(t.XmlNamespace("http://www.sbml.org/sbml/").version)

    def test_no_exceptions(self):
        t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2, version=4)
        t.XmlNamespace("http://www.sbml.org/sbml/level2/version4")
        t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2)
        t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", version=4)
        t.XmlNamespace("http://www.sbml.org/sbml/")

    def test_exceptions(self):
        with pytest.raises(t.XmlNamespaceVersionLevelMismatchException):
            t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2, version=3)
        with pytest.raises(t.XmlNamespaceVersionLevelMismatchException):
            t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=1, version=4)
        with pytest.raises(AttributeError):
            t.XmlNamespace(None)

    def test_cellml(self):
        c=t.XmlNamespace("http://www.cellml.org/cellml/1.0#")
        self.assertIsNone(c.level)
        self.assertIsNone(c.version)
        self.assertEqual("http://www.cellml.org/cellml/1.0#",c.namespace)

    def test_sedml(self):
        s=t.XmlNamespace("http://sed-ml.org/")
        self.assertIsNone(s.level)
        self.assertIsNone(s.version)
        self.assertEqual("http://sed-ml.org/", s.namespace)
