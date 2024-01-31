import random
from readers.article import Article

from generators.matching_qa_pair import MatchingQAPair
from readers.figure import Figure


class MatchingQAPairGenerator:

    def __init__(self, articles):
        self.articles = articles
        self.option_num = 4
        # list of list of figures chosen to get distractors from
        self.groups = []
        self.qaps = []
        self.generate()
        print("generated")

    def generate(self):
        self.select_groups()
        for group in self.groups:
            for figure in group:
                questions = Figure.get_contexts(figure)
                for question in questions:
                    # TODO: for some expansion since options to pick could be relative to reference
                    options = self.pick_options(group, figure)
                    random.shuffle(options)
                    self.qaps.append(MatchingQAPair(question, options, figure))

    # question: how to select options that are valuable as options of a question
    def select_groups(self):
        option_num = self.option_num
        waiting_list = []
        for article in self.articles:
            figures = Article.get_figures(article)
            if len(figures) >= option_num:
                self.groups.append(figures)
            else:
                waiting_list.extend(figures)
                if len(waiting_list) >= option_num:
                    self.groups.append(waiting_list)
                    waiting_list.clear()

    # return a list of figures where the first one is right answer
    def pick_options(self, group, correct_fig):
        distractors = group.copy()
        distractors.remove(correct_fig)
        chosen_distractors = random.sample(distractors, self.option_num - 1)
        chosen_distractors.insert(0, correct_fig)
        # chosen_distractors is now the options
        return chosen_distractors
