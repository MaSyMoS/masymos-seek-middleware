from unittest import TestCase

import masemiwa.listener.server_functions as t


class Test(TestCase):
    def test__add_status_to_message(self):
        self.assertEqual(("123 - abc", 123), t._add_status_to_message("abc", 123))
        self.assertEqual(("0 - abc", 0), t._add_status_to_message("abc"))
        self.assertEqual(("0 - unknown", 0), t._add_status_to_message())

    def test__abort_because_morre_queue_has_stopped(self):
        self.assertFalse(t._abort_because_morre_queue_has_stopped())
