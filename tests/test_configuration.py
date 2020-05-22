import os
import unittest

from Configuration import Configuration, ConfigKeys
from Definitions import Definitions


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        Definitions.CONFIG_FILE_PATH = os.path.join(Definitions.ROOT_DIR, 'tests', 'test_config.yml')
        self.classUnderTest = Configuration()

    def test_get(self):
        result = self.classUnderTest.get(ConfigKeys.enable_api)
        self.assertIs(result, True)

    def test_get_chilli_mode(self):
        result = self.classUnderTest.get(ConfigKeys.chilli_display_mode)
        self.assertIs(result, False)

    def test_get_display_mode(self):
        result = self.classUnderTest.get(ConfigKeys.default_display_mode)
        self.assertEqual(result, 'TORRENTS')
