from unittest import TestCase

import masemiwa.config as conf
import masemiwa.morre_gate.morre_network as t


class Test(TestCase):
    def test__prepare_url(self):
        conf.Configuration.MORRE_SERVER.set("http://myserver:1234")
        self.assertEqual("http://myserver:1234", conf.Configuration.MORRE_SERVER.value)
        self.assertEqual("http://myserver:1234/morre/model_update_service/holla", t._prepare_url("holla"))

        conf.Configuration.MORRE_SERVER.set("http://myserver:1234/directory")
        self.assertEqual("http://myserver:1234/directory", conf.Configuration.MORRE_SERVER.value)
        self.assertEqual("http://myserver:1234/directory/morre/model_update_service/holla2", t._prepare_url("holla2"))

        conf.Configuration.MORRE_SERVER.set("http://myserver:1234/directory/")
        self.assertEqual("http://myserver:1234/directory/", conf.Configuration.MORRE_SERVER.value)
        self.assertEqual("http://myserver:1234/directory//morre/model_update_service/holla2", t._prepare_url("holla2"))

    def test_process_response(self):
        response_valid1: dict = dict(ok=True)
        response_valid2: dict = dict(ok="tRue")
        response_invalid1: dict = dict(ok=False)
        response_invalid2: dict = dict(right=True)
        response_invalid3: dict = dict(ok="falSe")

        self.assertTrue(t.process_response(response_valid1))
        self.assertTrue(t.process_response(response_valid2))
        self.assertFalse(t.process_response(response_invalid1))
        self.assertFalse(t.process_response(response_invalid2))
        self.assertFalse(t.process_response(response_invalid3))
