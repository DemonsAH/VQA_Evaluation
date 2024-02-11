import string

import constants
import nltk
from nltk.tokenize import word_tokenize


class Shortener: 

    def __init__(self):
        self.max_words = constants.qasper_context_len
        self.max_subsent = constants.matching_caption_max_subsent

    def remove_fig_name(self, name):
        tokens = word_tokenize(name)
        # for tests
        # print(tokens)
        result = ''

        def is_num_with_dot(substring):
            parts = substring.split('.')
            if len(parts) < 2:
                return False
            if (parts[0] in constants.roman_nums or parts[0].isnumeric()) and parts[1] == '':
                return True
            else:
                return False

        def is_num(substring):
            return substring.isnumeric() or substring in constants.roman_nums

        for i in range(len(tokens) - 3):
            if tokens[i] in constants.qasper_fig_tab_tokens:
                if tokens[i + 1] == '.' or tokens[i + 1] == ':':
                    if is_num(tokens[i + 2]) or is_num_with_dot(tokens[i + 2]):
                        result = ' '.join(tokens[(i + 3):])
                if is_num(tokens[i + 1]) or is_num_with_dot(tokens[i + 1]):
                    if tokens[i + 2] == ":":
                        result = ' '.join(tokens[(i + 3):])
                    else:
                        result = ' '.join(tokens[(i + 2):])
                    break
        # if result == '':
        #     raise RuntimeError("fig token not detected.")
        return result

    def shorten_words(self, words):
        # nltk.download('punkt')  # Download the punkt tokenizer if not already downloaded
        tokens = word_tokenize(words)
        result_words = ''
        result_subsent = ''
        # cut until max sub-sentence count
        for i in range(len(tokens)):
            punctuation_count = 0
            # could change string.punctuation to comma and punkt
            if tokens[i] in string.punctuation:
                punctuation_count += 1
            if punctuation_count == self.max_subsent:
                result_subsent = ' '.join(tokens[:i])
                break
        # cut until max words count
        if len(tokens) >= self.max_words:
            result_words = ' '.join(tokens[:self.max_words + 1])
        # take the shorter one
        if result_subsent == '' and result_words == '':
            return words
        elif result_subsent == '':
            return result_words
        elif result_words == '':
            return result_subsent
        elif len(result_words) > len(result_subsent):
            return result_subsent
        else:
            return result_words

