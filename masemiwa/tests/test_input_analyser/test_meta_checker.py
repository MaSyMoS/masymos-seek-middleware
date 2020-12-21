import unittest
from unittest import TestCase

import pytest

import masemiwa.input_analyser.meta_checker as t
from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason
from masemiwa.input_analyser.beans import XmlNamespace, SeekContentBlob, SeekContentBlobType

if __name__ == '__main__':
    unittest.main()


class TestMime(unittest.TestCase):
    def test_string(self):
        self.assertFalse(t.MetaChecker._check_mime_type('wrong'))

    def test_number(self):
        # noinspection PyTypeChecker
        self.assertFalse(t.MetaChecker._check_mime_type(42))  # NOSONAR

    def test_wrong_mime(self):
        self.assertFalse(t.MetaChecker._check_mime_type('text/plain'))

    def test_right_mime(self):
        self.assertTrue(t.MetaChecker._check_mime_type('application/xml'))


class TestCheckNamespace(TestCase):
    def test_success(self):
        b: SeekContentBlob = SeekContentBlob({'content_type': 'blo', 'link': 'bla'})
        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4" />'))
        self.assertEqual(SeekContentBlobType.SBML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://www.sbml.org/sbml/level1/version42" />'))
        self.assertEqual(SeekContentBlobType.SBML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://www.sbml.org/sbml/level2/version23" />'))
        self.assertEqual(SeekContentBlobType.SBML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://sed-ml.org/level1/version1" />'))
        self.assertEqual(SeekContentBlobType.SEDML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://sed-ml.org/level1/version2" />'))
        self.assertEqual(SeekContentBlobType.SEDML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://www.cellml.org/cellml/1.0" />'))
        self.assertEqual(SeekContentBlobType.CELLML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://www.cellml.org/cellml/1.1" />'))
        self.assertEqual(SeekContentBlobType.CELLML, b.type)

        self.assertTrue(t.MetaChecker._check_namespace(b,
                                                       '<sbml xmlns="http://www.sbml.org/sbml/level2" level="2" version="1" />'))
        self.assertEqual(SeekContentBlobType.SBML, b.type)

    def test_fail(self):
        b: SeekContentBlob = SeekContentBlob({'content_type': 'blo', 'link': 'bla'})
        self.assertFalse(t.MetaChecker._check_namespace(b,
                                                        '<sbml xmlns="http://www.sbml.org/sbml/level3/version23" />'))
        self.assertIsNone(b.type)

        self.assertFalse(t.MetaChecker._check_namespace(b,
                                                        '<sbml xmlns="http://sed-ml.org/level1/version3" />'))
        self.assertIsNone(b.type)

        self.assertFalse(t.MetaChecker._check_namespace(b,
                                                        '<sbml xmlns="http://sed-ml.org" />'))
        self.assertIsNone(b.type)

        self.assertFalse(t.MetaChecker._check_namespace(b,
                                                        '<sbml xmlns="http://www.cellml.org/cellml" />'))
        self.assertIsNone(b.type)

        self.assertFalse(t.MetaChecker._check_namespace(b,
                                                        '<sbml xmlns="http://www.cellml.org/cellml/1.2" />'))
        self.assertIsNone(b.type)


class TestExtractNamespace(TestCase):
    namespace_valid1: str = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Created by Schorsch on 2011/04/04 15:53:02-->
<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">
<model name="Schorsch" >
</model></sbml>
"""

    def test_success(self):
        test: XmlNamespace = t.MetaChecker._extract_namespace(self.namespace_valid1)
        self.assertEqual("http://www.sbml.org/sbml/level2/version4", test.namespace)
        self.assertEqual(2, test.level)
        self.assertEqual(4, test.version)

        test = t.MetaChecker._extract_namespace(
            '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4" />')
        self.assertEqual("http://www.sbml.org/sbml/level2/version4", test.namespace)
        self.assertEqual(2, test.level)
        self.assertEqual(4, test.version)

        test = t.MetaChecker._extract_namespace(
            '<sbml version="4" xmlns="http://www.sbml.org/sbml/level2/version4" />')
        self.assertEqual("http://www.sbml.org/sbml/level2/version4", test.namespace)
        self.assertEqual(2, test.level)
        self.assertEqual(4, test.version)

        test = t.MetaChecker._extract_namespace(
            '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" />')
        self.assertEqual("http://www.sbml.org/sbml/level2/version4", test.namespace)
        self.assertEqual(2, test.level)
        self.assertEqual(4, test.version)

        test = t.MetaChecker._extract_namespace(
            '<yay xmlns="http://sed-ml.org" />')
        self.assertEqual("http://sed-ml.org", test.namespace)
        self.assertIsNone(test.level)
        self.assertIsNone(test.version)

    def test_trigger_error(self):
        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace(
                '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="3" />')
        self.assertEqual(InputAnalyseErrorReason.DATA_NAMESPACE_LEVEL_VERSION_MISMATCH, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace(
                '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="1" version="4" />')
        self.assertEqual(InputAnalyseErrorReason.DATA_NAMESPACE_LEVEL_VERSION_MISMATCH, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace(
                '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4a" />')
        self.assertEqual(InputAnalyseErrorReason.DATA_ATTRIBUTE_NOT_PARSABLE, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace(
                '<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2y" version="4" />')
        self.assertEqual(InputAnalyseErrorReason.DATA_ATTRIBUTE_NOT_PARSABLE, e.value.reason)

    def test_invalid_xml(self):
        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace("")
        self.assertEqual(InputAnalyseErrorReason.DATA_NOT_VALID_XML, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace("no XML")
        self.assertEqual(InputAnalyseErrorReason.DATA_NOT_VALID_XML, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace("<?xml!>")
        self.assertEqual(InputAnalyseErrorReason.DATA_NOT_VALID_XML, e.value.reason)

        with pytest.raises(InputAnalyseError) as e:
            t.MetaChecker._extract_namespace('>""')
        self.assertEqual(InputAnalyseErrorReason.DATA_NOT_VALID_XML, e.value.reason)
