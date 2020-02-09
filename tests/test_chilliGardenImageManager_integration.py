import os
import unittest
from PIL import Image

from ChilliGardenImageManager import ChilliGardenImageManager
from Definitions import Definitions


class TestChilliGardenImageManagerIntegration(unittest.TestCase):
    __reference_path_b = os.path.join(Definitions.ROOT_DIR, 'test_images/test_chilli_reference_image_black.png')
    __reference_path_c = os.path.join(Definitions.ROOT_DIR, 'test_images/test_chilli_reference_image_colour.png')
    __test_image_path_b = os.path.join(Definitions.ROOT_DIR, 'test_images/test_chilli_image_black.png')
    __test_image_path_c = os.path.join(Definitions.ROOT_DIR, 'test_images/test_chilli_image_colour.png')

    def setUp(self):
        if os.path.exists(self.__test_image_path_b):
            os.remove(self.__test_image_path_b)
        if os.path.exists(self.__test_image_path_c):
            os.remove(self.__test_image_path_c)

    def images_equal_references(self):
        return Image.open(self.__reference_path_b, 'r') == Image.open(self.__test_image_path_b, 'r') and \
                        Image.open(self.__reference_path_c, 'r') == Image.open(self.__test_image_path_c, 'r')

    def test_integration_test(self):
        chilli_manager = ChilliGardenImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)

        chilli_manager.add_title('Downloading:')
        chilli_manager.add_torrent('ubuntu_19-10.tar.gz', 60)
        chilli_manager.add_torrent('1another_veryveryveryveryveryveryveryveryveryvery_longlonglong_namename_is_here_dont_wait_for_me_to_stop\
        lets_get_past_the_line_limitasdjhflajdshflkjahdsflkjhadsflkasj.avi', 15)
        chilli_manager.add_title('Completed:')
        chilli_manager.add_torrent('test download name some_linux_distro-this_sentence_is_long.tar.gz', 100)
        chilli_manager.add_torrent('test download name some_linux_distro-this_sentence_is_long.gzip', 100)
        chilli_manager.add_torrent('yet_another_torrent_s01e05.avi', 100)
        chilli_manager.add_torrent('collection_of_free_classic_games.zip', 100)
        chilli_manager.add_torrent('yet_another_veryveryveryveryveryveryveryveryveryvery_longlonglong_namename_is_here_dont_wait_for_me_to_stop.avi', 100)

        chilli_manager.print_torrents_list()

        # There is certainly a better way to do this, but this is simple and works.
        chilli_manager.get_black_image().save(self.__test_image_path_b)
        chilli_manager.get_colour_image().save(self.__test_image_path_c)
        self.assertTrue(self.images_equal_references(), "INTEGRATION TEST FAILURE: Chilli Manager test images do not match references")


if __name__ == '__main__':
    unittest.main()
