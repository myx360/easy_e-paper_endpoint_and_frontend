import os
import unittest

from PIL import Image

from Definitions import Definitions
from EpaperImage import EpaperImage
from display__picture.PictureImageManager import PictureImageManager


class TestPictureImageManager(unittest.TestCase):
    __test_image_before_png = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/styled_deep_dream_before.png')
    __test_image_after_black_png = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/styled_deep_dream_after.png')
    __test_image_after_colour_png = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/styled_deep_dream_after_colour.png')
    __test_image_reference = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/test_reference_PIM.png')
    __test_image_reference_colour = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/test_reference_PIM_colour.png')

    def cleanup(self):
        if os.path.exists(self.__test_image_after_black_png):
            os.remove(self.__test_image_after_black_png)
        if os.path.exists(self.__test_image_after_colour_png):
            os.remove(self.__test_image_after_colour_png)

    def setUp(self):
        self.cleanup()
        self.classUnderTest = PictureImageManager()

    def tearDown(self):
        self.cleanup()

    def test_reset_to_background(self):
        self.classUnderTest._PictureImageManager__epaper_image = EpaperImage()
        self.classUnderTest.reset_to_background()
        self.assertEqual(self.classUnderTest._PictureImageManager__background,
                         self.classUnderTest._PictureImageManager__epaper_image)

    def test_integration_test(self):
        Definitions.READY_IMAGE_BLACK = self.__test_image_after_black_png
        Definitions.READY_IMAGE_COLOUR = self.__test_image_after_colour_png
        edited_image_png = self.classUnderTest.generate_display_image(self.__test_image_before_png)
        self.assertTrue(Image.open(self.__test_image_after_black_png) == Image.open(self.__test_image_reference))
        self.assertTrue(Image.open(self.__test_image_after_colour_png) == Image.open(self.__test_image_reference_colour))
        self.assertEqual(edited_image_png.image_black, self.classUnderTest.get_black_image())
        self.assertEqual(edited_image_png.image_colour, self.classUnderTest.get_colour_image())


if __name__ == '__main__':
    unittest.main()
