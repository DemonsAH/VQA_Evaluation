from evaluators.preprocessor import Preprocessor
from evaluators.shortener import Shortener
from readers.figure import Figure
from PIL import Image


class MatchingQAPair:

    def __init__(self, reference, options, answer):
        self.question = reference
        self.options = options
        self.answer = answer

    def get_options_img(self):
        result = []
        for option in self.options:
            image_path = Figure.get_dir(option)
            image_instance = Image.open(image_path)
            result.append(image_instance)
        return result

    def get_options_comp(self):
        result = []
        for option in self.options:
            result.append(Figure.get_caption(option))
        return result

    def get_options_comp_prep(self):
        result = []
        prep = Preprocessor()
        shortener = Shortener()
        for option in self.options:
            option_str = Figure.get_caption(option)
            result.append(Shortener.shorten_words(shortener, Preprocessor.process(prep, option_str)))
        return result

    def get_options_comp_prep_chal(self):
        shortener = Shortener()
        return Shortener.remove_fig_name(shortener, self.get_options_comp_prep())

    def get_options_dir(self):
        result = []
        for option in self.options:
            result.append(Figure.get_dir(option))
        return result

    # To judge if the given answer as an index is right.
    # Two figures here compared by caption
    def judge(self, given_answer):
        return Figure.get_caption(self.options[given_answer]) == Figure.get_caption(self.answer)
