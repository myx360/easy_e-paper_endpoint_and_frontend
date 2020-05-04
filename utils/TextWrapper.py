from PIL import Image, ImageDraw, ImageFont


class _WrappedLine(object):
    """Holder class for a wrapped line. Will only append text if it fits within line width.
    """

    def __init__(self, font: ImageFont, max_width: int, adding_whole_words: bool = True):
        self.__wrapped_line = ''
        self.__font = font
        self.__max_width = max_width
        self.__spaces_between_words = adding_whole_words
        self.__draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(100, 100)
            )
        )

    def _get_text_width(self, text: str):
        return self.__draw.textsize(
            text=text,
            font=self.__font
        )[0]

    def append_if_fits(self, text_to_add: str):
        text_fit = False
        if self.__spaces_between_words and not self.is_empty():
            proposal = self.__wrapped_line + ' ' + text_to_add
        else:
            proposal = self.__wrapped_line + text_to_add

        if self._get_text_width(proposal) < self.__max_width:
            self.__wrapped_line = proposal
            text_fit = True
        return text_fit

    def get_line(self):
        return self.__wrapped_line

    def is_empty(self):
        return self.__wrapped_line == ''


class _WrappedLines(object):
    """ Holder class where pre-wrapped lines of text are added. Will not append once max-lines is reached.
    """

    def __init__(self, max_lines):
        self.__lines = []
        self.__max_lines = max_lines

    def get_lines(self):
        return self.__lines

    def add_line(self, wrapped_line: _WrappedLine):
        if len(self.__lines) < self.__max_lines:
            self.__lines.append(wrapped_line.get_line())
            return True
        else:
            return False

    def is_full(self):
        return len(self.__lines) == self.__max_lines


class TextWrapper(object):
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """

    def __init__(self, text, font, max_width, max_lines=2):
        self.__text = text
        self.__text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n') if l
        ]
        self.__font = font
        self.__max_width = max_width
        self.__max_lines = max_lines
        self.__wrapped_lines = _WrappedLines(max_lines)

    def __add_large_word(self, word: str) -> str:
        """ Creates a wrapped line from words that are larger than one line
        :param word: word to add
        :return: returns the rest of the word that does not fit
        """
        characters = list(word)
        wrapped_line = _WrappedLine(self.__font, self.__max_width, False)

        for i, letter in enumerate(characters):
            if not wrapped_line.append_if_fits(letter):
                self.__wrapped_lines.add_line(wrapped_line)
                return ''.join(characters[i:len(characters)])

    def __add_word(self, wrapped_line: _WrappedLine, word: str):
        # word fits on line case
        if wrapped_line.append_if_fits(word):
            return wrapped_line

        # a single word is larger than one line edge case
        if wrapped_line.is_empty():
            remaining_chars = self.__add_large_word(word)
            if remaining_chars and not self.__wrapped_lines.is_full():
                return self.__add_word(_WrappedLine(self.__font, self.__max_width), remaining_chars)
            return wrapped_line

        # word pushes line over max width
        self.__wrapped_lines.add_line(wrapped_line)
        if self.__wrapped_lines.is_full():
            return wrapped_line
        return self.__add_word(_WrappedLine(self.__font, self.__max_width), word)

    def generate_wrapped_text(self) -> str:
        """ Generates text wrapped to line width and within number of lines
        :return: An string filled of lines that fit within box size for font and font size given
        """
        for line in self.__text_lines:
            wrapped_line = _WrappedLine(self.__font, self.__max_width)
            word_list = line.split(' ')

            for word in word_list:
                wrapped_line = self.__add_word(wrapped_line, word)

                if self.__wrapped_lines.is_full():
                    return '\n'.join(self.__wrapped_lines.get_lines())

            self.__wrapped_lines.add_line(wrapped_line)
        return '\n'.join(self.__wrapped_lines.get_lines())
