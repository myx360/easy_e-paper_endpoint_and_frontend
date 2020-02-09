from PIL import Image
from EpaperImage import EpaperImage
from Definitions import Definitions


# todo: needs static variables capitalised
class Images(object):

    pc100_black = Image.open(Definitions.PC100_BLACK_FILEPATH)
    pc100_colour = Image.open(Definitions.PC100_COLOUR_FILEPATH)
    pc66_black = Image.open(Definitions.PC66_BLACK_FILEPATH)
    pc66_colour = Image.open(Definitions.PC66_COLOUR_FILEPATH)
    pc33_black = Image.open(Definitions.PC33_BLACK_FILEPATH)
    pc33_colour = Image.open(Definitions.PC33_COLOUR_FILEPATH)
    pc0_black = Image.open(Definitions.PC0_BLACK_FILEPATH)

    background_black = Image.open(Definitions.BACKGROUND_BLACK_FILEPATH)
    background_colour = Image.open(Definitions.BACKGROUND_COLOUR_FILEPATH)
    epaper_chilli_background = EpaperImage(background_black.convert('1'), background_colour.convert('1'))

    plain_background = Image.new('L', (400, 300), 0)
    epaper_plain_background = EpaperImage(plain_background, plain_background)

    epaper_00pc = EpaperImage(pc0_black, None)
    epaper_33pc = EpaperImage(pc33_black, pc33_colour)
    epaper_66pc = EpaperImage(pc66_black, pc66_colour)
    epaper_100pc = EpaperImage(pc100_black, pc100_colour)
