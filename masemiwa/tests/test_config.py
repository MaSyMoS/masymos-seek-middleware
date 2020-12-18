from unittest import TestCase

import pytest

import masemiwa.config as config


class Test(TestCase):
    config_items: list = [item for item in config.Configuration]

    valid_conf1: list = [("connection_timeout", 42),
                         ("connection_timeout_morre", 1234),
                         ("MORRE_SERVER", "http://123.12.12.31:5432"),
                         ("log_configuration_file", "/my/folder/mimamu.configuration")]
    valid_conf2: list = [("CONNECTION_TIMEOUT", 42),
                         ("coNNection_timeout_morre", 1234),
                         ("log_CONFIGURATION_file", "/my/folder/mimamu.configuration")]
    invalid_conf1: list = [("unknown_key", 42)]
    invalid_conf2: list = [("connection_timeout_morre", "twenty-three")]

    def test__check_config_keys_and_values_valid1(self):
        r: list = config._check_config_keys_and_values(self.valid_conf1, self.config_items)
        self.assertTrue(list, type(r))
        self.assertEqual(4, len(r))
        for i in r:
            self.assertEqual(tuple, type(i))
            self.assertEqual(2, len(i))
            self.assertEqual(str, type(i[0]))

    def test__check_config_keys_and_values_valid2(self):
        r: list = config._check_config_keys_and_values(self.valid_conf2, self.config_items)
        self.assertTrue(list, type(r))
        self.assertEqual(3, len(r))
        for i in r:
            self.assertEqual(tuple, type(i))
            self.assertEqual(2, len(i))
            self.assertEqual(str, type(i[0]))

    def test__check_config_keys_and_values_invalid(self):
        with pytest.raises(config.ConfigurationFileException) as e:
            config._check_config_keys_and_values(self.invalid_conf1, self.config_items)
        self.assertTrue("defines an unknown key" in str(e))
        with pytest.raises(config.ConfigurationFileException) as e:
            config._check_config_keys_and_values(self.invalid_conf2, self.config_items)
        self.assertTrue("cannot be converted" in str(e))
