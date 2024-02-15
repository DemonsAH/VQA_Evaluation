import random
from readers.article import Article
from thefuzz import process
from thefuzz import fuzz
from generators.matching_qa_pair import MatchingQAPair
from readers.figure import Figure


class MatchingQAPairGenerator:

    def __init__(self, articles):
        self.articles = articles
        self.option_num = 4
        # list of lists of figures chosen to get distractors from
        self.groups = []
        self.qaps = []
        self.qaps_simi_cap = []
        self.select_groups()
        self.generate(self.groups, self.qaps)
        # self.generate_simi_cap()
        print("generated")

    def generate(self, groups, qaps):
        for group in groups:
            for figure in group:
                questions = Figure.get_contexts(figure)
                for question in questions:
                    # TODO: for some extension since options to pick could be relative to reference
                    options = self.pick_options(group, figure)
                    random.shuffle(options)
                    qaps.append(MatchingQAPair(question, options, figure))

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

    # To select groups based on the similarity between captions
    def generate_simi_cap(self):
        option_num = self.option_num
        all_figure_caps = []
        all_figure = []
        count = 0
        for article in self.articles:
            for figure in Article.get_figures(article):
                all_figure_caps.append(Figure.get_caption(figure))
                all_figure.append(figure)
        for article in self.articles:
            for figure in Article.get_figures(article):
                matches = process.extract(Figure.get_caption(figure), all_figure_caps, scorer=fuzz.token_sort_ratio)
                options = []
                j = 1
                for i in range(option_num - 1):
                    option_cand = matches[j][0]
                    if option_cand not in options:
                        options.append(option_cand)
                    j = j + 1
                # options = [match[0] for match in matches][:option_num]
                options_fig = []
                for option in options:
                    options_fig.append(all_figure[all_figure_caps.index(option)])
                options_fig.insert(0, figure)
                # get options with highest text similarity
                # if options[0] != Figure.get_caption(figure):
                #     if Figure.get_caption(figure) not in options:
                #         raise RuntimeError("Error by searching figure with caption")
                #     else:
                #         options_fig = self.pick_options(options_fig, figure)
                random.shuffle(options_fig)
                for ref in Figure.get_contexts(figure):
                    self.qaps_simi_cap.append(MatchingQAPair(ref, options_fig, figure))
            print(str(count) + "/6557")
            count = count + 1

    # return a list of figures where the first one is right answer
    def pick_options(self, group, correct_fig):
        distractors = group.copy()
        distractors.remove(correct_fig)
        chosen_distractors = random.sample(distractors, self.option_num - 1)
        chosen_distractors.insert(0, correct_fig)
        # chosen_distractors is now the options
        return chosen_distractors
