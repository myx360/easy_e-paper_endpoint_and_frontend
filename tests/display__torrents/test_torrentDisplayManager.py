import os
import unittest
import sys
from unittest.mock import patch, MagicMock, call

from Configuration import Configuration, ConfigKeys
from Definitions import Definitions
from EpaperImage import EpaperImage
from Images import Images

sys.modules['epaper.EpaperDisplay'] = MagicMock()  # prevents failures on TorrentDisplayManager import in dev testing

# Must appear below EpaperDisplay mock:
from display__torrents.ChilliGardenImageManager import ChilliGardenImageManager
from display__torrents.PlainTorrentImageManager import PlainTorrentImageManager
from display__torrents.TorrentDataManager import Torrent, Torrents
from display__torrents.TorrentDisplayManager import TorrentDisplayManager


class TestTorrentDisplayManager(unittest.TestCase):
    __TEST_TORRENT_1 = Torrent('torrent1', '72%', 'Downloading')
    __TEST_TORRENT_2 = Torrent('torrent2', '100%', 'Idle')
    __TEST_TORRENT_3 = Torrent('torrent3', '33%', 'Stopped')
    __TEST_TORRENT_4 = Torrent('torrent4', '50%', 'Downloading')

    def setUp(self):
        Definitions.CONFIG_FILE_PATH = os.path.join(Definitions.ROOT_DIR, 'tests', 'test_config.yml')
        self.__config = Configuration()
        self.__config._Configuration__config[ConfigKeys.transmission_user.name] = 'user'
        self.__config._Configuration__config[ConfigKeys.transmission_password.name] = 'pass'
        self.__TEST_TORRENTS_1 = Torrents()
        self.__TEST_TORRENTS_1.downloading = [self.__TEST_TORRENT_1]
        self.__TEST_TORRENTS_2 = Torrents()
        self.__TEST_TORRENTS_2.completed = [self.__TEST_TORRENT_2]
        self.__TEST_TORRENTS_2.stopped = [self.__TEST_TORRENT_3]
        self.__TEST_TORRENTS_2.downloading = [self.__TEST_TORRENT_4]

    def test_chilli_mode_is_default(self):
        class_under_test = TorrentDisplayManager(self.__config)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, ChilliGardenImageManager)

    def test_chilli_mode_True_uses_ChilliGardenManager(self):
        class_under_test = TorrentDisplayManager(self.__config, chilli_mode=True)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, ChilliGardenImageManager)

    def test_chilli_mode_False_uses_PlainTorrentImageManager(self):
        class_under_test = TorrentDisplayManager(self.__config, chilli_mode=False)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, PlainTorrentImageManager)

    @patch('display__torrents.TorrentDisplayManager.TorrentDataManager')
    def test_new_image_to_display(self, mock_data_manager):
        dm_instance = MagicMock()
        dm_instance.get_torrents.return_value = self.__TEST_TORRENTS_1
        mock_data_manager.return_value = dm_instance
        class_under_test = TorrentDisplayManager(self.__config)
        self.assertTrue(class_under_test.new_image_to_display(), 'first dataset should always trigger new_image_to_display')

        dm_instance.get_torrents.return_value = self.__TEST_TORRENTS_2
        self.assertTrue(class_under_test.new_image_to_display(), 'new dataset should trigger new_image_to_display')

        dm_instance.get_torrents.return_value = self.__TEST_TORRENTS_2
        self.assertFalse(class_under_test.new_image_to_display(), 'same dataset should not trigger new_image_to_display')

    @patch('display__torrents.TorrentDisplayManager.ChilliGardenImageManager', autospec=True)
    def test_update_display(self, mock_image_manager):
        mock, mock_im_instance, mock_epd = MagicMock(), MagicMock(), MagicMock()
        mock.im_instance, mock.epd = mock_im_instance, mock_epd

        mock_image_manager.return_value = mock_im_instance
        test_epaper_image = EpaperImage(Images.epaper_00pc, Images.epaper_00pc)
        mock_im_instance.generate_display_image.return_value = test_epaper_image

        class_under_test = TorrentDisplayManager(self.__config, chilli_mode=True)
        class_under_test._TorrentDisplayManager__torrents = self.__TEST_TORRENTS_2
        class_under_test.update_display(mock_epd)

        mock.assert_has_calls([call.im_instance.reset_to_background(),
                               call.im_instance.add_title('Downloading:'),
                               call.im_instance.add_torrent('torrent4', 50.0),
                               call.im_instance.add_title('Completed:'),
                               call.im_instance.add_torrent('torrent2', 100.0),
                               call.im_instance.add_title('Stopped:'),
                               call.im_instance.add_torrent('torrent3', 33.0),
                               call.im_instance.generate_display_image(),
                               call.epd.safe_display(test_epaper_image)])

    def test_set_image_manager_to_chilli(self):
        class_under_test = TorrentDisplayManager(self.__config, chilli_mode=True)
        class_under_test.set_image_manager(True)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, ChilliGardenImageManager)

    def test_set_image_manager(self):
        class_under_test = TorrentDisplayManager(self.__config, chilli_mode=True)
        class_under_test.set_image_manager(False)
        self.assertIsInstance(class_under_test._TorrentDisplayManager__image_manager, PlainTorrentImageManager)

    def test_printable_name(self):
        class_under_test = TorrentDisplayManager(self.__config)
        self.assertEqual(class_under_test.printable_name(), 'Torrent display - displays torrents returned by Transmission client')

    def test_can_register_happy_path(self):
        class_under_test = TorrentDisplayManager(self.__config)
        self.assertTrue(class_under_test.can_register())

    def test_can_register_no_username(self):
        del self.__config._Configuration__config[ConfigKeys.transmission_user.name]
        del self.__config._Configuration__config[ConfigKeys.transmission_password.name]
        class_under_test = TorrentDisplayManager(self.__config)
        self.assertFalse(class_under_test.can_register())


if __name__ == '__main__':
    unittest.main()
