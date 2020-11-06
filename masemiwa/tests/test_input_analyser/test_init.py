from unittest import TestCase

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason


class TestInputAnalyseError(TestCase):
    def test_success(self):
        e = InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_NAMESPACE_NOT_SUPPORTED, "http://my.url/file.xyz")
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_NAMESPACE_NOT_SUPPORTED, e.reason)
        self.assertEqual(type(e.reason.value), str)
        self.assertNotEqual(e.reason.value.strip(), "")
        self.assertEqual(e.reason.value, e.message)
        self.assertEqual("http://my.url/file.xyz", e.resource)

        e = InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_MIME_NOT_SUPPORTED)
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_MIME_NOT_SUPPORTED, e.reason)
        self.assertEqual(type(e.reason.value), str)
        self.assertNotEqual(e.reason.value.strip(), "")
        self.assertEqual(e.reason.value, e.message)
        self.assertIsNone(e.resource)
