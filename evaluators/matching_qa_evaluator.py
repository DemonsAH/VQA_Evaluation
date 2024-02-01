import json

from PIL import Image
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration

import constants
from evaluators.preprocessor import Preprocessor
from evaluators.shortener import Shortener
from generators.matching_qa_generator import MatchingQAPairGenerator
from generators.matching_qa_pair import MatchingQAPair
from readers.figure import Figure


def get_option_symbols():
    option_num = constants.matching_option_num
    start = 65
    symbols = []
    end = chr(start + option_num - 1)
    for i in range(65, 65 + option_num):
        symbols.append(chr(i))
    return symbols, end


def matching_write_json(qap_dicts):
    with open(constants.matching_write_json_path, 'w') as r:
        json.dump(qap_dicts, r, indent=4)
        # for qap_dict in qap_dicts:
        #     json.dump(qap_dict, r, indent=4)
    r.close()


class MatchingQAEvaluator:

    def __init__(self, articles):
        self.generator = MatchingQAPairGenerator(articles)
        self.qaps = self.generator.qaps
        self.blank_png = Image.open(constants.blank_png_dir)
        self.preprocessor = Preprocessor()
        self.shortener = Shortener()

    def evaluate(self):
        # qap_count = 0
        # qap_correct = 0
        # qap_comp_correct = 0
        qap_dicts = []
        for qap in self.qaps:
            qap_dict = {}
            # option_num = len(qap.options)
            # symbols, end = get_option_symbols()
            prep_question = Shortener.shorten_words(self.shortener, Preprocessor.process(self.preprocessor, qap.question))
            # heading = "Give the order of the right figure that match the given reference:"
            prefix = "Here is a description of a figure:\n"
            surfix = "\nAnswer this multiple choice question: Based on the provided description of a figure, please select the most suitable image. Answer only with the option ID. Here are the options:"
            prefix_comp = "Here is a description of an image:\n"
            # surfix_comp = "\nPlease select one from following captions(0 or 1 or 2 or 3) which fits the given description best."
            surfix_comp = "\nAnswer this multiple choice question: Based on the provided description of a figure, please select the most suitable caption. Answer only with the option ID. Here are the options:"
            # answer = self.run_model(prefix + qap.question + surfix, MatchingQAPair.get_options(qap))
            # adding questions element
            qap_dict['question'] = prefix + qap.question + surfix
            qap_dict['question_comp'] = prefix_comp + qap.question + surfix_comp
            qap_dict['question_prep'] = prefix + prep_question + surfix
            qap_dict['question_comp_prep'] = prefix_comp + prep_question + surfix_comp
            qap_dict['reference'] = qap.question
            qap_dict['reference_prep'] = prep_question
            # adding options into elements
            options_comp = MatchingQAPair.get_options_comp(qap)
            options_comp_prep = MatchingQAPair.get_options_comp_prep(qap)
            answer_comp = ""
            for i in range(len(options_comp)):
                if options_comp[i] == Figure.get_caption(qap.answer):
                    answer_comp = chr(i + 65)
                options_comp[i] = chr(i + 65) + ". " + options_comp[i]
            for j in range(len(options_comp_prep)):
                options_comp_prep[j] = chr(j + 65) + ". " + options_comp_prep[j]
            options_dir = MatchingQAPair.get_options_dir(qap)
            qap_dict['options'] = options_dir
            qap_dict['options_comp'] = options_comp
            qap_dict['options_comp_prep'] = options_comp_prep
            qap_dict['answer'] = Figure.get_dir(qap.answer)
            qap_dict['answer_comp'] = answer_comp
            qap_dicts.append(qap_dict)
        matching_write_json(qap_dicts)
            # answer_comp = self.run_model(question_comp, self.blank_png)
            # qap_count += 1
            # if MatchingQAPair.judge(qap, answer):
            #     qap_correct += 1
            # int_answer_comp = int(answer_comp)
            # if MatchingQAPair.judge(qap, int_answer_comp):
            #     qap_comp_correct += 1
            # break
        # return qap_correct, qap_comp_correct, qap_count

    # def run_model(self, question, figures):
    #     print("question: " + question)
    #     # for figure in figures:
    #     #     figure.show()
    #     # return 1
    #     processor = Pix2StructProcessor.from_pretrained('google/matcha-chartqa')
    #     model = Pix2StructForConditionalGeneration.from_pretrained('google/matcha-chartqa')
    #     inputs = processor(images=figures, text=question, return_tensors="pt")
    #     predictions = model.generate(**inputs, max_new_tokens=512)
    #     output = processor.decode(predictions[0], skip_special_tokens=True)
    #     print("answer: " + output)
    #     return output
