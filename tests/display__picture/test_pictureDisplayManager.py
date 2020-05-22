import os
import sys
import unittest
from threading import Lock
from unittest.mock import patch, MagicMock, call
from shutil import copyfile

from EpaperImage import EpaperImage
from Images import Images
from Definitions import Definitions

sys.modules['epaper.EpaperDisplay'] = MagicMock()  # prevents failures on TorrentDisplayManager import in dev testing
# Must appear below EpaperDisplay mock:
from display__picture.PictureDisplayManager import PictureDisplayManager
from DisplayManager import DisplayMode


class TestPictureDisplayManager(unittest.TestCase):

    TEST_IMAGE_DOES_NOT_EXIST = os.path.join(Definitions.ROOT_DIR, 'tests', 'DOES_NOT_EXIST')
    BLACK_TEST_PNG = os.path.join(Definitions.ROOT_DIR, 'tests', 'test_images', 'test_image_black.png')
    COLOUR_TEST_PNG = os.path.join(Definitions.ROOT_DIR, 'tests', 'test_images', 'test_image_colour.png')

    def cleanup(self):
        if os.path.isfile(self.BLACK_TEST_PNG):
            os.remove(self.BLACK_TEST_PNG)
        if os.path.isfile(self.COLOUR_TEST_PNG):
            os.remove(self.COLOUR_TEST_PNG)

    def tearDown(self):
        self.cleanup()

    def setUp(self):
        self.cleanup()

    def test_get_mode(self):
        self.assertIs(PictureDisplayManager.get_mode(), DisplayMode.IMAGE)

    @patch('display__picture.PictureDisplayManager.PictureImageManager', autospec=True)
    def test_update_display_with_pre_generated(self, mock_image_manager):
        mock, mock_im_instance, mock_epd = MagicMock(), MagicMock(), MagicMock()
        mock.im_instance, mock.epd = mock_im_instance, mock_epd

        mock_image_manager.return_value = mock_im_instance
        test_epaper_image = EpaperImage(Images.epaper_00pc, Images.epaper_00pc)
        mock_im_instance.get_epaper_image.return_value = test_epaper_image

        image_lock = Lock()
        class_under_test = PictureDisplayManager(image_lock)
        class_under_test.update_display(mock_epd)
        mock.assert_has_calls([call.epd.safe_display(test_epaper_image)])

    @patch('display__picture.PictureDisplayManager.PictureImageManager', autospec=True)
    def test_update_display_from_filepath(self, mock_image_manager):
        mock, mock_im_instance, mock_epd = MagicMock(), MagicMock(), MagicMock()
        mock.im_instance, mock.epd = mock_im_instance, mock_epd

        mock_image_manager.return_value = mock_im_instance
        empty_epaper_image = EpaperImage()
        mock_im_instance.get_epaper_image.return_value = empty_epaper_image

        test_epaper_image = EpaperImage(MagicMock(), MagicMock())
        mock_im_instance.generate_display_image.return_value = test_epaper_image

        Definitions.READY_IMAGE_BLACK = Definitions.PC33_BLACK_FILEPATH
        Definitions.READY_IMAGE_COLOUR = Definitions.PC33_COLOUR_FILEPATH

        image_lock = Lock()
        class_under_test = PictureDisplayManager(image_lock)

        class_under_test.update_display(mock_epd)
        mock.assert_has_calls([call.epd.safe_display(test_epaper_image)])

    @patch('display__picture.PictureDisplayManager.PictureImageManager', autospec=True)
    def test_new_image_to_display(self, mock_image_manager):
        Definitions.TEMP_IMAGE_BLACK = self.TEST_IMAGE_DOES_NOT_EXIST
        Definitions.TEMP_IMAGE_COLOUR = self.TEST_IMAGE_DOES_NOT_EXIST

        copyfile(Definitions.PC33_BLACK_FILEPATH, self.BLACK_TEST_PNG)
        copyfile(Definitions.PC33_COLOUR_FILEPATH, self.COLOUR_TEST_PNG)

        mock_im_instance = MagicMock()
        mock_image_manager.return_value = mock_im_instance

        test_epaper_image = EpaperImage(MagicMock(), MagicMock())
        mock_im_instance.get_epaper_image.return_value = test_epaper_image

        image_lock = Lock()
        class_under_test = PictureDisplayManager(image_lock)

        Definitions.TEMP_IMAGE_BLACK = self.BLACK_TEST_PNG
        Definitions.TEMP_IMAGE_COLOUR = self.COLOUR_TEST_PNG

        self.assertTrue(class_under_test.new_image_to_display(False))

        mock_im_instance.assert_has_calls([call.reset_to_background(),
                                           call.generate_display_image(Definitions.TEMP_IMAGE_BLACK, Definitions.TEMP_IMAGE_COLOUR),
                                           call.get_epaper_image()])

        self.assertFalse(os.path.isfile(Definitions.TEMP_IMAGE_BLACK))
        self.assertFalse(os.path.isfile(Definitions.TEMP_IMAGE_COLOUR))

    @patch('display__picture.PictureDisplayManager.PictureImageManager', autospec=True)
    def test_new_image_to_display_identical_to_current(self, mock_image_manager):
        Definitions.TEMP_IMAGE_BLACK = self.TEST_IMAGE_DOES_NOT_EXIST
        Definitions.TEMP_IMAGE_COLOUR = self.TEST_IMAGE_DOES_NOT_EXIST

        copyfile(Definitions.PC33_BLACK_FILEPATH, self.BLACK_TEST_PNG)
        copyfile(Definitions.PC33_COLOUR_FILEPATH, self.COLOUR_TEST_PNG)

        mock_im_instance = MagicMock()
        mock_image_manager.return_value = mock_im_instance

        test_epaper_image = EpaperImage(MagicMock(), MagicMock())
        mock_im_instance.generate_display_image.return_value = test_epaper_image
        mock_im_instance.get_epaper_image.return_value = test_epaper_image

        image_lock = Lock()
        class_under_test = PictureDisplayManager(image_lock)

        Definitions.TEMP_IMAGE_BLACK = self.BLACK_TEST_PNG
        Definitions.TEMP_IMAGE_COLOUR = self.COLOUR_TEST_PNG

        class_under_test._PictureDisplayManager__current_image = test_epaper_image
        self.assertFalse(class_under_test.new_image_to_display(False))

        mock_im_instance.assert_has_calls([call.reset_to_background(),
                                           call.generate_display_image(Definitions.TEMP_IMAGE_BLACK, Definitions.TEMP_IMAGE_COLOUR),
                                           call.get_epaper_image()])

        self.assertFalse(os.path.isfile(Definitions.TEMP_IMAGE_BLACK))
        self.assertFalse(os.path.isfile(Definitions.TEMP_IMAGE_COLOUR))

    @patch('display__picture.PictureDisplayManager.PictureImageManager', autospec=True)
    def test_new_image_to_display_identical_to_current_with_force_flag(self, mock_image_manager):
        Definitions.TEMP_IMAGE_BLACK = self.TEST_IMAGE_DOES_NOT_EXIST
        Definitions.TEMP_IMAGE_COLOUR = self.TEST_IMAGE_DOES_NOT_EXIST

        copyfile(Definitions.PC33_BLACK_FILEPATH, self.BLACK_TEST_PNG)
        copyfile(Definitions.PC33_COLOUR_FILEPATH, self.COLOUR_TEST_PNG)

        mock_im_instance = MagicMock()
        mock_image_manager.return_value = mock_im_instance

        test_epaper_image = EpaperImage(MagicMock(), MagicMock())
        mock_im_instance.generate_display_image.return_value = test_epaper_image
        mock_im_instance.get_epaper_image.return_value = test_epaper_image

        image_lock = Lock()
        class_under_test = PictureDisplayManager(image_lock)

        Definitions.TEMP_IMAGE_BLACK = self.BLACK_TEST_PNG
        Definitions.TEMP_IMAGE_COLOUR = self.COLOUR_TEST_PNG

        class_under_test._PictureDisplayManager__current_image = test_epaper_image
        self.assertTrue(class_under_test.new_image_to_display(True))

        mock_im_instance.assert_has_calls([call.reset_to_background(),
                                           call.generate_display_image(Definitions.TEMP_IMAGE_BLACK, Definitions.TEMP_IMAGE_COLOUR),
                                           call.get_epaper_image()])

        self.assertFalse(os.path.isfile(Definitions.TEMP_IMAGE_BLACK))
        self.assertFalse(os.path.isfile(Definitions.TEMP_IMAGE_COLOUR))

    def test_printable_name(self):
        class_under_test = PictureDisplayManager(Lock())
        self.assertEqual(class_under_test.printable_name(), 'Image display - crops, resizes and anti-aliases a black and/or a colour image.')

    def test_can_register(self):
        class_under_test = PictureDisplayManager(Lock())
        self.assertTrue(class_under_test.can_register())


if __name__ == '__main__':
    unittest.main()
