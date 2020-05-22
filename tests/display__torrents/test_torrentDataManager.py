import os
import unittest

from Definitions import Definitions
from custom_errors.ScriptFailureError import ScriptFailureError
from display__torrents.TorrentDataManager import TorrentDataManager, Torrent, Torrents


class TestTorrentDataManager(unittest.TestCase):

    __TEST_USER_NAME = 'user'
    __TEST_PASSWORD = 'pass'

    __STOPPED_1 = Torrent('ubuntu-18.04.3-desktop-amd64.iso', '0%', 'Stopped')
    __DOWNLOADING_1 = Torrent('ubuntu-16.04-live-server-amd64.iso', '72%', 'Downloading')
    __DOWNLOADING_2 = Torrent('a_further_torrent-pushing_the_line_limit_boundaries_for_the_epaper_module1080p60.s10e05.avi', '48%', 'Downloading')
    __COMPLETED_1 = Torrent('ubuntu-19.10-live-server-amd64.iso', '100%', 'Idle')

    __FAIL_SCRIPT = os.path.join(Definitions.ROOT_DIR, 'scripts', 'fail_script.sh')
    __FAKE_TORRENT_DATA_SCRIPT = os.path.join(Definitions.ROOT_DIR, 'scripts', 'fake_torrent_data.sh')
    __STANDARD_BASH_COMMAND = Definitions.GET_TORRENT_SCRIPT_PATH + ' {0} {1}'.format(__TEST_USER_NAME, __TEST_PASSWORD)

    def setUp(self):
        self.torrent_data_manager = TorrentDataManager(self.__TEST_USER_NAME, self.__TEST_PASSWORD)

    def test_TorrentDataManager_init(self):
        self.assertEqual(self.__STANDARD_BASH_COMMAND, self.torrent_data_manager._TorrentDataManager__bash_command)
        self.assertTrue(Definitions.GET_TORRENT_SCRIPT in self.__STANDARD_BASH_COMMAND)
        self.assertTrue(self.__TEST_USER_NAME in self.__STANDARD_BASH_COMMAND)
        self.assertTrue(self.__TEST_PASSWORD in self.__STANDARD_BASH_COMMAND)

    def test_get_torrents_and_Torrents_equality(self):
        self.torrent_data_manager._TorrentDataManager__bash_command = self.__FAKE_TORRENT_DATA_SCRIPT
        result = self.torrent_data_manager.get_torrents()

        expected_result = Torrents()
        expected_result.stopped = [self.__STOPPED_1]
        expected_result.completed = [self.__COMPLETED_1]
        expected_result.downloading = [self.__DOWNLOADING_1, self.__DOWNLOADING_2]

        self.assertEqual(result, expected_result)

        self.assertEqual(result.stopped[0], self.__STOPPED_1)
        self.assertEqual(result.completed[0], self.__COMPLETED_1)
        self.assertTrue(self.__DOWNLOADING_1 in result.downloading
                        and self.__DOWNLOADING_2 in result.downloading)

    def test_get_torrents_fails(self):
        self.torrent_data_manager._TorrentDataManager__bash_command = self.__FAIL_SCRIPT
        self.assertRaises(ScriptFailureError, self.torrent_data_manager.get_torrents)


if __name__ == '__main__':
    unittest.main()
