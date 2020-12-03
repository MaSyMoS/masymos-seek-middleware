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
