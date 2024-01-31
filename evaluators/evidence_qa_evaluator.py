import json

import requests
from PIL import Image
from nltk.translate.bleu_score import sentence_bleu
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration

import constants
from evaluators.preprocessor import Preprocessor


# To write a list of dict into a json file
def evi_write_json(qap_dicts):
    with open(constants.evi_write_json_path, 'w') as r:
        json.dump(qap_dicts, r, indent=4)
        # for qap_dict in qap_dicts:
        #     json.dump(qap_dict, r, indent=4)
    r.close()


class EviQAEvaluator:

    def __init__(self, articles):
        self.articles = articles
        self.preprocessor = Preprocessor()
        # self.processor = Pix2StructProcessor.from_pretrained('google/matcha-chartqa')
        # self.model = Pix2StructForConditionalGeneration.from_pretrained('google/matcha-chartqa')

    # actually outputting qaps in json file
    def evaluate(self):
        qap_count = 0
        bleu_scores = []
        qap_dicts = []
        for article in self.articles:
            for qap in article.fig_qaps:
                question_prep = Preprocessor.process(self.preprocessor, qap.question)
                qap_dict = {
                            'question': qap.question,
                            'answer': qap.answer,
                            'dir': qap.figure.fig_dir,
                            'question_prep': question_prep
                            }
                qap_dicts.append(qap_dict)

                # print("dir: " + qap.figure.fig_dir)
                # print("question: " + qap.question)
                # print("correct answer: " + qap.answer)
                # qap_count += 1
                # # evaluate this question answer pair
                # model_answer = self.run_model(qap.figure, qap.question, qap.answer)
                # # 将参考文本和生成文本转为标记化的列表
                # reference_tokens = model_answer.split()
                # generated_tokens = qap.answer.split()
                # # 计算BLEU分数
                # bleu_score = sentence_bleu(reference_tokens, generated_tokens)
                # bleu_scores.append(bleu_score)
        evi_write_json(qap_dicts)
        return

    # def run_model(self, figure, question, answer):
        # This model is not working. writing question and answer out.

        # image = Image.open(figure.fig_dir)
        # # url = "https://raw.githubusercontent.com/vis-nlp/ChartQA/main/ChartQA%20Dataset/val/png/20294671002019.png"
        # # image = Image.open(requests.get(url, stream=True).raw)
        # inputs = self.processor(images=image, text=question, return_tensors="pt")
        # predictions = self.model.generate(**inputs, max_new_tokens=512)
        # result = self.processor.decode(predictions[0], skip_special_tokens=True)
        # return result

