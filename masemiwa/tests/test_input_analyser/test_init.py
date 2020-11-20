from unittest import TestCase

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason


class TestInputAnalyseError(TestCase):
    def test_success(self):
        e = InputAnalyseError(InputAnalyseErrorReason.DATA_NAMESPACE_NOT_SUPPORTED, "http://my.url/file.xyz")
        self.assertEqual(InputAnalyseErrorReason.DATA_NAMESPACE_NOT_SUPPORTED, e.reason)
        self.assertEqual(str, type(e.reason.error_message))
        self.assertNotEqual("",e.reason.error_message.strip())
        self.assertEqual("http://my.url/file.xyz", e.resource)

        e = InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_MIME_NOT_SUPPORTED)
        self.assertEqual(InputAnalyseErrorReason.CONTENT_BLOB_MIME_NOT_SUPPORTED, e.reason)
        self.assertEqual(str, type(e.reason.error_message))
        self.assertNotEqual("",e.reason.error_message.strip())
        self.assertIsNone(e.resource)
