import requests
from PIL import Image
from nltk.translate.bleu_score import sentence_bleu
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration


class EviQAEvaluator:

    def __init__(self, articles):
        self.articles = articles
        self.processor = Pix2StructProcessor.from_pretrained('google/matcha-chartqa')
        self.model = Pix2StructForConditionalGeneration.from_pretrained('google/matcha-chartqa')

    def evaluate(self):
        qap_count = 0
        bleu_scores = []
        for article in self.articles:
            for qap in article.fig_qaps:
                print("qap: " + qap)
                print("question: " + qap.question)
                print("correct answer: " + qap.amswer)
                qap_count += 1
                # evaluate this question answer pair
                model_answer = self.run_model(qap.figure, qap.question)
                # 将参考文本和生成文本转为标记化的列表
                reference_tokens = model_answer.split()
                generated_tokens = qap.amswer.split()
                # 计算BLEU分数
                bleu_score = sentence_bleu(reference_tokens, generated_tokens)
                bleu_scores.append(bleu_score)
        return bleu_scores

    def run_model(self, figure, question):
        image = Image.open(figure.fig_dir)
        # url = "https://raw.githubusercontent.com/vis-nlp/ChartQA/main/ChartQA%20Dataset/val/png/20294671002019.png"
        # image = Image.open(requests.get(url, stream=True).raw)
        inputs = self.processor(images=image, text=question, return_tensors="pt")
        predictions = self.model.generate(**inputs, max_new_tokens=512)
        result = self.processor.decode(predictions[0], skip_special_tokens=True)
        return result
