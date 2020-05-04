import os

from PIL import ImageFont


class Definitions(object):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    CONFIG_FILE_PATH = os.path.join(ROOT_DIR, 'config.yml')

    GET_TORRENT_SCRIPT = 'get_torrent_data.sh'
    GET_TORRENT_SCRIPT_PATH = os.path.join(ROOT_DIR, 'scripts', GET_TORRENT_SCRIPT)

    FONT_FILEPATH_SWANSEA = os.path.join(ROOT_DIR, 'fonts', 'Swansea-q3pd.ttf')
    FONT_FILEPATH_SWANSEA_BOLD = os.path.join(ROOT_DIR, 'fonts', 'SwanseaBold-D0ox.ttf')

    TEXT_FONT = ImageFont.truetype(FONT_FILEPATH_SWANSEA, 12)
    BOLD_FONT = ImageFont.truetype(FONT_FILEPATH_SWANSEA_BOLD, 12)

    PC100_BLACK_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_B.bmp')
    PC100_COLOUR_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_C.bmp')
    PC66_BLACK_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_66_B.bmp')
    PC66_COLOUR_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_66_C.bmp')
    PC33_BLACK_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_33_B.bmp')
    PC33_COLOUR_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_33_C.bmp')
    PC0_BLACK_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_percent_icon_pixel_00_B.bmp')
    BACKGROUND_BLACK_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_torrent_box_B.bmp')
    BACKGROUND_COLOUR_FILEPATH = os.path.join(ROOT_DIR, 'images', 'chilli_torrent_box_C.bmp')

    UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')
    TEMP_IMAGE_BLACK = os.path.join(ROOT_DIR, 'temp_black.png')
    TEMP_IMAGE_COLOUR = os.path.join(ROOT_DIR, 'temp_colour.png')
    READY_IMAGE_BLACK = os.path.join(ROOT_DIR, 'display_black.png')
    READY_IMAGE_COLOUR = os.path.join(ROOT_DIR, 'display_colour.png')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
    DISPLAY_SIZE = 400, 300
