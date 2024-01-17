from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from readers.figure import Figure


class MQAGGenerator:

    def __init__(self, articles):
        self.articles = articles
        self.tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")

    def generate(self):
        qnas = []
        for article in self.articles:
            for fig in article.get_figures():
                for refs in fig.get_contexts():
                    for ref in refs:
                        inputs = self.tokenizer(ref, return_tensors="pt")
                        outputs = self.model.generate(**inputs, max_length=100)
                        question_answer = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
                        question_answer = question_answer.replace(self.tokenizer.pad_token, "").replace(self.tokenizer.eos_token,
                                                                                                   "")
                        question, answer = question_answer.split(self.tokenizer.sep_token)
                        new_qna = QnA(question, answer, fig)
                        qnas.append(new_qna)
        return qnas


class QnA:

    def __init__(self, question, answer, figure):
        self.question = question
        self.answer = answer
        self.fig = figure

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_figure(self):
        return self.fig
