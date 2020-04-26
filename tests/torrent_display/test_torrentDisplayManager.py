import unittest
import sys
from unittest.mock import patch, MagicMock, call

from torrent_display.TorrentDataManager import Torrent, Torrents

sys.modules['epaper.EpaperDisplay'] = MagicMock()  # prevents failures on TorrentDisplayManager import in dev testing

# Must appear below EpaperDisplay mock:
from torrent_display.ChilliGardenImageManager import ChilliGardenImageManager
from torrent_display.PlainTorrentImageManager import PlainTorrentImageManager
from torrent_display.TorrentDisplayManager import TorrentDisplayManager


class TestTorrentDisplayManager(unittest.TestCase):
    __TEST_USERNAME = "user11"
    __TEST_PASSWORD = "pass22"
    __TEST_TORRENT_1 = Torrent('torrent1', '72%', 'Downloading')
    __TEST_TORRENT_2 = Torrent('torrent2', '100%', 'Idle')
    __TEST_TORRENT_3 = Torrent('torrent3', '33%', 'Stopped')
    __TEST_TORRENT_4 = Torrent('torrent4', '50%', 'Downloading')

    def setUp(self):
        self.__TEST_TORRENTS_1 = Torrents()
        self.__TEST_TORRENTS_1.downloading = [self.__TEST_TORRENT_1]
        self.__TEST_TORRENTS_2 = Torrents()
        self.__TEST_TORRENTS_2.completed = [self.__TEST_TORRENT_2]
        self.__TEST_TORRENTS_2.stopped = [self.__TEST_TORRENT_3]
        self.__TEST_TORRENTS_2.downloading = [self.__TEST_TORRENT_4]

    def test_chilli_mode_is_default(self):
        class_under_test = TorrentDisplayManager(self.__TEST_USERNAME, self.__TEST_PASSWORD)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, ChilliGardenImageManager)

    def test_chilli_mode_True_uses_ChilliGardenManager(self):
        class_under_test = TorrentDisplayManager(self.__TEST_USERNAME, self.__TEST_PASSWORD, chilli_mode=True)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, ChilliGardenImageManager)

    def test_chilli_mode_False_uses_PlainTorrentImageManager(self):
        class_under_test = TorrentDisplayManager(self.__TEST_USERNAME, self.__TEST_PASSWORD, chilli_mode=False)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, PlainTorrentImageManager)

    @patch('torrent_display.TorrentDisplayManager.TorrentDataManager')
    def test_new_image_to_display(self, mock_data_manager):
        dm_instance = MagicMock()
        dm_instance.get_torrents.return_value = self.__TEST_TORRENTS_1
        mock_data_manager.return_value = dm_instance
        class_under_test = TorrentDisplayManager(self.__TEST_USERNAME, self.__TEST_PASSWORD)
        self.assertTrue(class_under_test.new_image_to_display(), 'first dataset should always trigger new_image_to_display')

        dm_instance.get_torrents.return_value = self.__TEST_TORRENTS_2
        self.assertTrue(class_under_test.new_image_to_display(), 'new dataset should trigger new_image_to_display')

        dm_instance.get_torrents.return_value = self.__TEST_TORRENTS_2
        self.assertFalse(class_under_test.new_image_to_display(), 'same dataset should not trigger new_image_to_display')

    @patch('torrent_display.TorrentDisplayManager.ChilliGardenImageManager', autospec=True)
    def test_update_display(self, mock_image_manager):
        mock, mock_im_instance, mock_epd = MagicMock(), MagicMock(), MagicMock()
        mock.im_instance, mock.epd = mock_im_instance, mock_epd

        mock_image_manager.return_value = mock_im_instance
        mock_im_instance.get_black_image.return_value = 'black_image'
        mock_im_instance.get_colour_image.return_value = 'colour_image'

        class_under_test = TorrentDisplayManager(self.__TEST_USERNAME, self.__TEST_PASSWORD, chilli_mode=True)
        class_under_test._TorrentDisplayManager__torrents = self.__TEST_TORRENTS_2
        class_under_test.update_display(mock_epd)

        mock.assert_has_calls([call.im_instance.reset_image_to_background(),
                               call.im_instance.add_title('Downloading:'),
                               call.im_instance.add_torrent('torrent4', 50.0),
                               call.im_instance.add_title('Completed:'),
                               call.im_instance.add_torrent('torrent2', 100.0),
                               call.im_instance.add_title('Stopped:'),
                               call.im_instance.add_torrent('torrent3', 33.0),
                               call.im_instance.generate_display_image(),
                               call.im_instance.get_black_image(),
                               call.im_instance.get_colour_image(),
                               call.epd.safe_display('black_image', 'colour_image')])


if __name__ == '__main__':
    unittest.main()
