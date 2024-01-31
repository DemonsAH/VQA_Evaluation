import re
from word2number import w2n


class Preprocessor:

    def convert_words_to_numbers(self, sentence):
        # 使用正则表达式找到所有包含数字单词的部分
        pattern = re.compile(r'\b(?:' + '|'.join(w2n.words) + r')\b', re.IGNORECASE)
        matches = re.finditer(pattern, sentence)

        # 逐一替换每个匹配项为对应的阿拉伯数字
        for match in matches:
            word = match.group()
            arabic_number = w2n.word_to_num(word)
            sentence = sentence.replace(word, str(arabic_number))

        return sentence

    # 示例
    # input_sentence = "I have twenty apples and fifteen oranges."
    # output_sentence = convert_words_to_numbers(input_sentence)
    # print(f"原始句子: {input_sentence}")
    # print(f"转换后句子: {output_sentence}")

    def __init__(self):
        self.lowercase_switch = True
        self.num_convert_switch = True
        self.remove_periods_switch = True
        self.remove_articles_switch = True
        self.add_apostrophe_switch = True
        self.replace_punctuation_switch = True

    def set_switches(self, lowercase, num_convert, rm_periods, rm_articles, add_apo, rpl_punct):
        self.lowercase_switch = lowercase
        self.num_convert_switch = num_convert
        self.remove_periods_switch = rm_periods
        self.remove_articles_switch = rm_articles
        self.add_apostrophe_switch = add_apo
        self.replace_punctuation_switch = rpl_punct

    def process(self, string):
        if not isinstance(string, str):
            raise RuntimeError("Input for process() should be str. ")
        temp = string
        if self.lowercase_switch:
            temp = temp.lower()
        elif self.num_convert_switch:
            # TODO test the function
            temp = self.convert_words_to_numbers(temp)
        elif self.remove_periods_switch:
            temp = temp.replace('. ', ' ')
        elif self.remove_articles_switch:
            temp = temp.replace(' a ', ' ')
            temp = temp.replace(' an ', ' ')
            temp = temp.replace(' the ', ' ')
        elif self.add_apostrophe_switch:
            temp = temp.replace(' dont ', ' don\'t')
            temp = temp.replace(' cant ', ' can\'t')
            temp = temp.replace(' wont ', ' won\'t')
            temp = temp.replace(' shouldnt ', ' shouldn\'t')
            temp = temp.replace(' im ', ' i\'m')
            temp = temp.replace(' youre ', ' you\'re')
            temp = temp.replace(' shes ', ' she\'s')
            temp = temp.replace(' hes ', ' he\'s')
            temp = temp.replace(' wouldve ', ' would\'ve')
            # more replacement needed or use an API for that
        elif self.replace_punctuation_switch:
            translator = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
            temp = temp.translate(translator)
        return temp

