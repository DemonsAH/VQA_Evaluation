import string

import constants
import nltk
from nltk.tokenize import word_tokenize


class Shortener: 

    def __init__(self):
        self.max_words = constants.qasper_context_len
        self.max_subsent = constants.matching_caption_max_subsent

    def shorten_words(self, words):
        nltk.download('punkt')  # Download the punkt tokenizer if not already downloaded
        tokens = word_tokenize(words)
        for i in range(len(tokens)):
            punctation_count = 0
            if tokens[i] in string.punctation:
                punctation_count += 1
            if punctation_count == self.max_subsent:
                result_subsent = ''.join(tokens[:i])
                break
        result_words = ''.join(tokens[:self.max_words + 1])
        if len(result_subsent) >= len(result_words):
            return result_words
        else:
            return result_subsent

