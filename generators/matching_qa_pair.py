from readers.figure import Figure
from PIL import Image


class MatchingQAPair:

    def __init__(self, reference, options, answer):
        self.question = reference
        self.options = options
        self.answer = answer

    def get_options(self):
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

    # To judge if the given answer as an index is right.
    # Two figures here compared by caption
    def judge(self, given_answer):
        return Figure.get_caption(self.options[given_answer]) == Figure.get_caption(self.answer)
