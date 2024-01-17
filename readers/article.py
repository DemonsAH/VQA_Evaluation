import regex as re
import constants
from readers.figure import Figure
from readers.qa_pair import QAPair
import nltk


def get_context_token(words, str):
    # nltk.download('punkt')
    lbound = 0
    result = ""
    direction = -1
    sentences = nltk.sent_tokenize(words)
    for sentence in sentences:
        if str in sentence:
            lbound = sentences.index(sentence)
            rbound = sentences.index(sentence)
            result = sentence
    while (lbound > 0 or rbound < len(sentences) - 1) and len(result) < constants.qasper_context_len:
        if direction == -1 and lbound > 0:
            neighbor_sent = sentences[lbound + direction]
            if (not exist_ref(neighbor_sent)) and len(result) + len(neighbor_sent) <= constants.qasper_context_len:
                result = neighbor_sent + result
                lbound -= 1
            else:
                lbound = 0
                continue
            direction *= -1

        elif direction == 1 and rbound < len(sentences) - 1:
            neighbor_sent = sentences[rbound + direction]
            if (not exist_ref(neighbor_sent)) and len(result) + len(neighbor_sent) <= constants.qasper_context_len:
                result += neighbor_sent
                rbound += 1
            else:
                rbound = len(sentences) - 1
                continue
            direction *= -1
        else:
            direction *= -1
    return result


def exist_ref(sentence):
    # result = (re.search(sentence, constants.qasper_fig_pattern) is not None) or (re.match(sentence, constants.qasper_tab_pattern) is not None)
    result = (constants.qasper_fig_token not in sentence) and (constants.qasper_tab_token not in sentence)
    return result


# a simple implementation of tokenizer, only count constant words in context and ignore pure comma, point etc.
def get_context(words, str):
    count = constants.qasper_context_len
    index = words.index(str)
    context = str
    # left = math.ceil(count/2)
    left_border = index
    # right = int(count/2)
    right_border = index
    direction = 1
    while count > 0 and (right_border < len(words) - 1 or left_border > 0):
        if direction == 1:
            if right_border >= len(words) - 1:
                direction *= -1
                continue
            context = context + " " + words[right_border + 1]
            if re.match(r'\.$|,$|\?$|!$|\\$|\*$|\($|\)$', words[right_border + 1]) is None:
                count -= 1
                direction *= -1
            right_border += 1
        if direction == -1:
            if left_border <= 0:
                direction *= -1
                continue
            context = words[left_border - 1] + " " + context
            if re.match(r'\.$|,$|\?$|!$|\\$|\*$|\($|\)$', words[left_border - 1]) is None:
                count -= 1
                direction *= -1
            left_border -= 1
    # TODO cut the first and last uncompleted sentence
    return context


class Article:

    def __init__(self, figures, abstract, text, num, qas):
        self.missing_fig_num = 0
        self.fig_and_tab_text = figures
        self.abstract = abstract
        self.full_text = text
        self.num = num
        # a list of tables and figures referenced in this paper
        self.figures = []
        self.tables = []
        # a dict of ref number of figures such as T
        self.contexts_figure = {}
        self.contexts_table = {}
        self.ref_qas = {}
        self.qas = qas
        self.fig_qaps = []
        # patterns used in this class. All for reference detection in evidence
        # and first two also for reference detection in full text.
        self.patterns = ['TABREF([0-9]*)(.*)',
                         'FIGREF([0-9]*)(.*)',
                         'FLOAT SELECTED: (.*)']
        self.analyze_figures()
        self.search_qas()

    # detect all figures and tables in the full text and create class Figure for them
    def analyze_figures(self):
        # print(type(self.figures)) ->list
        for figure in self.fig_and_tab_text:
            fig_num = figure["file"]
            fig_dir = constants.qasper_png_base_dir + "\\" + self.num + "\\" + fig_num
            # To get the directory and caption of a figure to create a figure instance
            # as a first step
            new_figure = Figure(fig_dir, figure["caption"])
            # See if it is a table and settle it to the right list
            if re.match(r'.*Table.*', fig_num) is not None:
                Figure.set_is_table(new_figure)
                self.tables.append(new_figure)
            else:
                self.figures.append(new_figure)

        # Save figures and tables separately for possible further use
        fig_names = self.search("FIGREF", self.contexts_figure)
        tab_names = self.search("TABREF", self.contexts_table)
        for i in range(len(self.contexts_figure)):
            # Figure.add_context(self.figures[i], self.contexts_figure[fig_names[i]])
            try:
                self.figures[i].add_context(self.contexts_figure[fig_names[i]])
                self.figures[i].set_name(fig_names[i])
            except IndexError:
                # print(self.num + "--current i:" + str(i) + "--tab_names size" + str(len(tab_names)))
                self.missing_fig_num += 1
        for j in range(len(self.contexts_table)):
            # Figure.add_context(self.tables[j], self.contexts_table[tab_names[j]])
            try:
                self.tables[j].add_context(self.contexts_table[tab_names[j]])
                self.figures[j].set_name(tab_names[j])
            except IndexError:
                # print(self.num + "--current j:" + str(j) + "--tab_names size" + str(len(tab_names)))
                self.missing_fig_num += 1
        return

    # To search target str(could only be TABREF or FIGREF here) from the full text
    # and get the reference
    def search(self, str, contexts):
        # TODO If same reference comes in short distance even in one sentence,
        #  no need of generating questions for every reference.
        names = []
        for section in self.full_text:
            for paragraph in section['paragraphs']:
                # found a reference in a paragraph
                if str in paragraph:
                    words = paragraph.split()
                    for word in words:
                        # get the real ref info like TABREF28
                        pattern = "(" + str + '[0-9]*)(.*)'
                        if re.match(pattern, word) is not None:
                            name = re.search(pattern, word).group(1)
                            context = get_context_token(paragraph, word)
                            if name in contexts:
                                contexts[name].append(context)
                            else:
                                contexts[name] = [context]
                                names.append(name)
                    break
        return names

    def get_figures(self):
        result = self.figures + self.tables
        return result

    def get_qas(self):
        return self.fig_qaps

    # str here could just be TABREF or FIGREF
    # to search if there are references of figures or tables in the evidence of a given question.
    def search_qas(self):
        for qa in self.qas:
            question = qa["question"]
            answers = qa["answers"]
            # For further use: keyword "free_form_answer" is for the true answer.
            for answer in answers:
                # since evidence includes always the whole paragraph
                # we use here highlight evidence to ensure that every sentence is about the question
                for evidence in answer["answer"]["evidence"]:
                    for pattern in self.patterns:
                        match_fig = self.evi_match_fig(evidence, pattern)
                        if match_fig is not None:
                            new_qap = QAPair(question, answer["answer"]["free_form_answer"], evidence, match_fig)
                            self.fig_qaps.append(new_qap)

    # To match evidence with given pattern and return figure name or caption.
    def evi_match_fig(self, evidence, pattern):
        if re.match(pattern, evidence) is not None:
            name = re.search(pattern, evidence).group(1)
            return self.search_name(name)

    # for the another token recognition, not used now
    def evi_match_fig_token(self, evidence, str):
        pattern = str + '.*'
        if re.match(pattern, evidence) is not None:
            name = re.search(pattern, evidence).group(1)
            return self.search_name(name)

    # search a figure with its name (e.g. Table 1: xxx)
    def search_name(self, name):
        for fig in self.figures:
            if (Figure.get_name(fig) == name) | (Figure.get_caption(fig) == name):
                return fig
        for tab in self.tables:
            if (Figure.get_name(tab) == name) | (Figure.get_caption(tab) == name):
                return tab
        return None


