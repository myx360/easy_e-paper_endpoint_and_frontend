import os

from PIL import ImageFont

from display__torrents.PlainTorrentImageManager import PlainTorrentImageManager
from Definitions import Definitions


try:
    __reference_path_b = os.path.join(Definitions.ROOT_DIR, 'tests', 'test_images', 'test_plain_reference_image_black.png')
    __reference_path_c = os.path.join(Definitions.ROOT_DIR, 'tests', 'test_images', 'test_plain_reference_image_colour.png')

    if os.path.exists(__reference_path_b):
        os.remove(__reference_path_b)
    if os.path.exists(__reference_path_c):
        os.remove(__reference_path_c)

    plain_manager = PlainTorrentImageManager(ImageFont.truetype(Definitions.FONT_FILEPATH_SWANSEA, 12),
                                             ImageFont.truetype(Definitions.FONT_FILEPATH_SWANSEA_BOLD, 12))
    plain_manager.add_title('Downloading:')
    plain_manager.add_torrent('ubuntu_19-10.tar.gz', 60)
    plain_manager.add_torrent('1another_veryveryveryveryveryveryveryveryveryvery_longlonglong_namename_is_here_dont_wait_for_me_to_stop\
    lets_get_past_the_line_limitasdjhflajdshflkjahdsflkjhadsflkasj.avi', 15)
    plain_manager.add_title('Completed:')
    plain_manager.add_torrent('test download name some_linux_distro-this_sentence_is_long.tar.gz', 100)
    plain_manager.add_torrent('test download name some_linux_distro-this_sentence_is_long.gzip', 100)
    plain_manager.add_torrent('yet_another_torrent_s01e05.avi', 100)
    plain_manager.add_torrent('collection_of_free_classic_games.zip', 100)
    plain_manager.add_torrent('yet_another_veryveryveryveryveryveryveryveryveryvery_longlonglong_namename_is_here_dont_wait_for_me_to_stop.avi', 100)
    plain_manager.generate_display_image()
    plain_manager.get_black_image().save(__reference_path_b)
    plain_manager.get_colour_image().save(__reference_path_c)

except:
    print('ERROR! Could not write a new test image')
    exit(1)
