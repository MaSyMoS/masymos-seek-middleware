import copy
from unittest import TestCase

import pytest

import masemiwa.input_analyser.beans
import masemiwa.input_analyser.beans as t
from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason
from masemiwa.input_analyser.beans import SeekContentBlobType, SeekUrl


class TestSeekUrlObject(TestCase):
    def test_success(self):
        obj = masemiwa.input_analyser.beans.SeekUrl('https://fairdomhub.org/models/24.json?version=3')
        self.assertEqual('https://fairdomhub.org/models/24', obj.url)
        self.assertEqual(24, obj.id)

    def test_inkscape(self):
        with pytest.raises(InputAnalyseError) as e:
            masemiwa.input_analyser.beans.SeekUrl('inkscape.org')
        self.assertEqual(InputAnalyseErrorReason.URL_INVALID, e.value.reason)

    def test_incomplete(self):
        with pytest.raises(InputAnalyseError) as e:
            masemiwa.input_analyser.beans.SeekUrl('https://fairdomhub.org/models/')
        self.assertEqual(InputAnalyseErrorReason.URL_INVALID, e.value.reason)

    # noinspection PyPropertyAccess
    def test_readonly_attributes(self):
        obj: SeekUrl = masemiwa.input_analyser.beans.SeekUrl('https://fairdomhub.org/models/24.json?version=3')
        with pytest.raises(AttributeError):
            obj.id = 42
        with pytest.raises(AttributeError):
            obj.url = "test"


class TestSeekContentBlob(TestCase):
    valid_blob1 = {'content_type': 'blo', 'link': 'bla'}
    valid_blob2 = {'content_type': 'blo', 'link': 'my.website/bla/blo/42/blu/content_blob/4711?parameter=true'}

    def test_success(self):
        cb = t.SeekContentBlob(self.valid_blob1)
        self.assertEqual('blo', cb.mime)
        self.assertEqual('bla', cb.link)

    def test_exceptions(self):
        # test valid_blob first
        t.SeekContentBlob(self.valid_blob1)

        tmp: dict
        # content_type missing
        tmp = copy.deepcopy(self.valid_blob1)
        tmp.pop('content_type')
        with pytest.raises(InputAnalyseError) as e:
            t.SeekContentBlob(tmp)
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_CONTENT_INVALID, e.value.reason)

        # link missing
        tmp = copy.deepcopy(self.valid_blob1)
        tmp.pop('link')
        with pytest.raises(InputAnalyseError) as e:
            t.SeekContentBlob(tmp)
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_CONTENT_INVALID, e.value.reason)

        tmp: dict
        # content_type empty
        tmp = copy.deepcopy(self.valid_blob1)
        tmp['content_type'] = ''
        with pytest.raises(InputAnalyseError) as e:
            t.SeekContentBlob(tmp)
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_CONTENT_INVALID, e.value.reason)

        # link empty
        tmp = copy.deepcopy(self.valid_blob1)
        tmp['link'] = ''
        with pytest.raises(InputAnalyseError) as e:
            t.SeekContentBlob(tmp)
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_CONTENT_INVALID, e.value.reason)

    def test_type(self):
        b = t.SeekContentBlob(self.valid_blob1)
        self.assertIsNone(b.type)
        b.set_type(SeekContentBlobType.SBML)
        self.assertEqual(SeekContentBlobType.SBML, b.type)
        self.assertNotEqual(SeekContentBlobType.CELLML, b.type)

    def test_link(self):
        b = t.SeekContentBlob(self.valid_blob2)
        self.assertEqual("my.website/bla/blo/42/blu/content_blob/4711?parameter=true", b.link)
        self.assertEqual("my.website/bla/blo/42/blu", b.link_to_model)


class TestSeekJson(TestCase):
    valid_json: dict = {'data': {'id': '1234',
                                 'attributes': {'latest_version': '5',
                                                'content_blobs': [{'content_type': '42', 'link': 'yay'}]}}}

    def test_success(self):
        s = t.SeekJson(self.valid_json)
        self.assertEqual(1234, s.id)
        self.assertEqual(5, s.latest_version)
        self.assertEqual('yay', s.content_blobs[0].link)

    def test_exceptions(self):
        # no exception with valid data
        t.SeekJson(self.valid_json)

        tmp: dict
        # last version missing
        tmp = copy.deepcopy(self.valid_json)
        tmp['data']['attributes'].pop('latest_version')
        with pytest.raises(InputAnalyseError) as e:
            t.SeekJson(tmp)
        self.assertEqual(InputAnalyseErrorReason.JSON_CONTENT_INVALID, e.value.reason)

        # id missing
        tmp = copy.deepcopy(self.valid_json)
        tmp['data'].pop('id')
        with pytest.raises(InputAnalyseError) as e:
            t.SeekJson(tmp)
        self.assertEqual(InputAnalyseErrorReason.JSON_CONTENT_INVALID, e.value.reason)

        # id alphanumeric
        tmp = copy.deepcopy(self.valid_json)
        tmp['data']['id'] = "a38"
        with pytest.raises(InputAnalyseError) as e:
            t.SeekJson(tmp)
        self.assertEqual(InputAnalyseErrorReason.JSON_CONTENT_INVALID, e.value.reason)

        # version alphanumeric
        tmp = copy.deepcopy(self.valid_json)
        tmp['data']['attributes']['latest_version'] = "eof"
        with pytest.raises(InputAnalyseError) as e:
            t.SeekJson(tmp)
        self.assertEqual(InputAnalyseErrorReason.JSON_CONTENT_INVALID, e.value.reason)


class TestXmlNamespace(TestCase):

    def test__extract_level_version_from_namespace(self):
        self.assertEqual(2, t.XmlNamespace._extract_level_version_from_namespace(
            "http://www.sbml.org/sbml/level2/version4")[0])
        self.assertEqual(4, t.XmlNamespace._extract_level_version_from_namespace(
            "http://www.sbml.org/sbml/level2/version4")[1])
        self.assertEqual(None,
                         t.XmlNamespace._extract_level_version_from_namespace("http://www.sbml.org/sbml/version4")[0])
        self.assertEqual(4,
                         t.XmlNamespace._extract_level_version_from_namespace("http://www.sbml.org/sbml/version4")[1])
        self.assertEqual(2, t.XmlNamespace._extract_level_version_from_namespace("http://www.sbml.org/sbml/level2")[0])
        self.assertEqual(None,
                         t.XmlNamespace._extract_level_version_from_namespace("http://www.sbml.org/sbml/level2")[1])
        self.assertEqual(None, t.XmlNamespace._extract_level_version_from_namespace("http://www.sbml.org/sbml/")[0])
        self.assertEqual(None, t.XmlNamespace._extract_level_version_from_namespace("http://www.sbml.org/sbml/")[0])

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
        with pytest.raises(InputAnalyseError) as e:
            t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=2, version=3)
        self.assertEqual(InputAnalyseErrorReason.DATA_NAMESPACE_LEVEL_VERSION_MISMATCH, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.XmlNamespace("http://www.sbml.org/sbml/level2/version4", level=1, version=4)
        self.assertEqual(InputAnalyseErrorReason.DATA_NAMESPACE_LEVEL_VERSION_MISMATCH, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            # noinspection PyTypeChecker
            t.XmlNamespace(None)
        self.assertEqual(InputAnalyseErrorReason.DATA_NAMESPACE_EMPTY, e.value.reason)

    def test_cellml(self):
        c = t.XmlNamespace("http://www.cellml.org/cellml/1.0#")
        self.assertIsNone(c.level)
        self.assertIsNone(c.version)
        self.assertEqual("http://www.cellml.org/cellml/1.0#", c.namespace)

    def test_sedml(self):
        s = t.XmlNamespace("http://sed-ml.org/")
        self.assertIsNone(s.level)
        self.assertIsNone(s.version)
        self.assertEqual("http://sed-ml.org/", s.namespace)
