import unittest
from PIL import ImageFont

from Definitions import Definitions
import TextWrapper


class TestTextWrapper(unittest.TestCase):
    def setUp(self):
        self.test_font = ImageFont.truetype(Definitions.FONT_FILEPATH_SWANSEA, 12)

    def test_generate_wrapped_text(self):
        test_text = 'test_text'
        self.class_under_test = TextWrapper.TextWrapper(test_text, self.test_font, 200)
        self.assertEqual(self.class_under_test.generate_wrapped_text(), test_text)

    def test_generate_wrapped_text_multi_line(self):
        test_text = 'this sentence should be split nicely between lines.'
        expected_result = 'this sentence\nshould be split\nnicely between\nlines.'
        self.class_under_test = TextWrapper.TextWrapper(test_text, self.test_font, 100, 4)
        self.assertEqual(self.class_under_test.generate_wrapped_text(), expected_result)

    def test_generate_wrapped_text_long_word(self):
        test_text = 'this_is_a_very_long_word_that_goes_over_the_line_width_limit'
        expected_result = 'this_is_a_very_long_word_that_goe\ns_over_the_line_width_limit'
        self.class_under_test = TextWrapper.TextWrapper(test_text, self.test_font, 200)
        self.assertEqual(self.class_under_test.generate_wrapped_text(), expected_result)

    def test_generate_wrapped_text_multi_line_long_word(self):
        test_text = 'this_is_a_very_long_word_that_goes_over_the_line_width_limit'
        expected_result = 'this_is_a_very_lo\nng_word_that_go\nes_over_the_line\n_width_limit'
        self.class_under_test = TextWrapper.TextWrapper(test_text, self.test_font, 100, 4)
        self.assertEqual(self.class_under_test.generate_wrapped_text(), expected_result)

    def test_generate_wrapped_text_should_handle_preset_line_breaks(self):
        test_text = 'This sentence...\n....has a line break already but we should add a new one in the right place.'
        expected_result = 'This sentence...\n....has a line break already but we\nshould add a new one in the right'
        self.class_under_test = TextWrapper.TextWrapper(test_text, self.test_font, 200, 3)
        self.assertEqual(self.class_under_test.generate_wrapped_text(), expected_result)


if __name__ == '__main__':
    unittest.main()
