from PIL import Image
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration

import constants
from generators.matching_qa_generator import MatchingQAPairGenerator
from generators.matching_qa_pair import MatchingQAPair


def get_option_symbols():
    option_num = constants.matching_option_num
    start = 65
    symbols = []
    end = chr(start + option_num - 1)
    for i in range(65, 65 + option_num):
        symbols.append(chr(i))
    return symbols, end


class MatchingQAEvaluator:

    def __init__(self, articles):
        self.generator = MatchingQAPairGenerator(articles)
        self.qaps = self.generator.qaps
        self.blank_png = Image.open(constants.blank_png_dir)

    def evaluate(self):
        qap_count = 0
        qap_correct = 0
        qap_comp_correct = 0
        for qap in self.qaps:
            option_num = len(qap.options)
            symbols, end = get_option_symbols()
            # heading = "Give the order of the right figure that match the given reference:"
            prefix = "Which image corresponds to the description:"
            surfix = "Please select the image number (A-%s)." % end
            prefix_comp = "Here is a description of an image:\n"
            # surfix_comp = "\nPlease select one from following captions(0 or 1 or 2 or 3) which fits the given description best."
            surfix_comp = "\nBased on the provided description of an image, please select the most suitable caption. Provide only the identifier(an integer) of the chosen option. Here are the options:"
            # answer = self.run_model(prefix + qap.question + surfix, MatchingQAPair.get_options(qap))
            question_comp = prefix_comp + qap.question + surfix_comp
            options = MatchingQAPair.get_options_comp(qap)
            for i in range(len(options)):
                question_comp += "\n" + str(i + 1) + ". " + options[i]
            answer_comp = self.run_model(question_comp, self.blank_png)
            qap_count += 1
            # if MatchingQAPair.judge(qap, answer):
            #     qap_correct += 1
            int_answer_comp = int(answer_comp)
            if MatchingQAPair.judge(qap, int_answer_comp):
                qap_comp_correct += 1
            break
        return qap_correct, qap_comp_correct, qap_count

    def run_model(self, question, figures):
        print("question: " + question)
        # for figure in figures:
        #     figure.show()
        # return 1
        processor = Pix2StructProcessor.from_pretrained('google/matcha-chartqa')
        model = Pix2StructForConditionalGeneration.from_pretrained('google/matcha-chartqa')
        inputs = processor(images=figures, text=question, return_tensors="pt")
        predictions = model.generate(**inputs, max_new_tokens=512)
        output = processor.decode(predictions[0], skip_special_tokens=True)
        print("answer: " + output)
        return output
