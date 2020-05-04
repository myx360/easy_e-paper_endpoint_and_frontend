import os
import unittest

from PIL import Image

from Definitions import Definitions
from EpaperImage import EpaperImage
from display__picture.PictureImageManager import PictureImageManager


class TestPictureImageManager(unittest.TestCase):
    __test_image_before_png = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/styled_deep_dream_before.png')
    __test_image_after_png = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/styled_deep_dream_after.png')
    __test_image_after_colour_png = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/styled_deep_dream_after_colour.png')
    __test_image_reference = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/test_reference_PIM.png')
    __test_image_reference_colour = os.path.join(Definitions.ROOT_DIR, 'tests/test_images/test_reference_PIM_colour.png')

    def setUp(self):
        self.classUnderTest = PictureImageManager()
        if os.path.exists(self.__test_image_after_png):
            os.remove(self.__test_image_after_png)

    def test_reset_to_background(self):
        self.classUnderTest._PictureImageManager__epaper_image = EpaperImage()
        self.classUnderTest.reset_to_background()
        self.assertEqual(self.classUnderTest._PictureImageManager__background,
                         self.classUnderTest._PictureImageManager__epaper_image)

    def test_integration_test(self):
        editted_image_png = self.classUnderTest.generate_display_image(self.__test_image_before_png)
        editted_image_png.image_black.save(self.__test_image_after_png)
        editted_image_png.image_colour.save(self.__test_image_after_colour_png)
        self.assertTrue(Image.open(self.__test_image_after_png) == Image.open(self.__test_image_reference))
        self.assertTrue(Image.open(self.__test_image_after_colour_png) == Image.open(self.__test_image_reference_colour))
        self.assertEqual(editted_image_png.image_black, self.classUnderTest.get_black_image())
        self.assertEqual(editted_image_png.image_colour, self.classUnderTest.get_colour_image())


if __name__ == '__main__':
    unittest.main()
