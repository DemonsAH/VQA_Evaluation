import regex as re
from transformers import pipeline

from PIL import Image
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration

import constants
from evaluators.evidence_qa_evaluator import EviQAEvaluator
from evaluators.matching_qa_evaluator import MatchingQAEvaluator
from evaluators.shortener import Shortener
from generators.mqag_generator import MQAGGenerator
from readers.article import Article
from readers.figure import Figure
from readers.qasper_reader import QasperReader
# import nltk

def BLIP_test():
    import requests
    from PIL import Image
    from transformers import Blip2Processor, Blip2ForConditionalGeneration

    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")

    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    question = "how many dogs are in the picture?"
    inputs = processor(raw_image, question, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True).strip())


def general_test():
    # vertex_ai_init(None, None)
    # vertex_ai_test()
    # first step to test qasper
    articles = qasper_read_test()
    # BLIP_test()
    # calculate and show some basic infos about qasper
    # count_and_show(articles)
    seperate()
    matching_qap_test(articles)
    # mqag_generate_test()
    evidence_qap_test(articles)
    # test_str = "A. fig. 3: dev set wers for density ratio lm scaling factor vs. sequence length scaling factor . here."
    # test_shortener = Shortener()
    # result = Shortener.remove_fig_name(test_shortener, test_str)
    # print("result:" + result)
    # TODO some regex test demo
    # text = "FIGREF1gui"
    # print(re.match(r'(.*)FIGREF([0-9]+)(.*)', text))


    # TODO demo test for tokenizer
    # text = "This is a sample text. It has multiple sentences."
    # nltk.download('punkt')  # 下载必要的数据，如分词器所需的数据
    # sentences = nltk.sent_tokenize(text)

    # stanfordnlp.download('en')
    # nlp = stanfordnlp.Pipeline()
    #
    # sentences = nlp.sent_tokenize(text)

    # print(sentences)

    # TODO demo test for one matching task

    # TODO squad
    # from transformers import pipeline
    #
    # qa_pipeline = pipeline(
    #     "question-answering",
    #     model="csarron/bert-base-uncased-squad-v1",
    #     tokenizer="csarron/bert-base-uncased-squad-v1"
    # )
    #
    # predictions = qa_pipeline({
    #     'context': "Here is a description of an image:\nAs illustrated in Figure FIGREF1, our key idea is that we can exploit discourse relations BIBREF4 to efficiently propagate polarity from seed predicates that directly report one's emotions (e.g., “to be glad” is positive).",
    #     'question': "Based on the provided description in the context, please select the most suitable option as a caption for this image. Here are the options:"
    #                 "\nA: Examples of polarity scores predicted by the BiGRU model trained with AL+CA+CO."
    #                 "\nB: An overview of our method. We focus on pairs of events, the former events and the latter events, which are connected with a discourse relation, CAUSE or CONCESSION. Dropped pronouns are indicated by brackets in English translations. We divide the event pairs into three types: AL, CA, and CO. In AL, the polarity of a latter event is automatically identified as either positive or negative, according to the seed lexicon (the positive word is colored red and the negative word blue). We propagate the latter event’s polarity to the former event. The same polarity as the latter event is used for the discourse relation CAUSE, and the reversed polarity for CONCESSION. In CA and CO, the latter event’s polarity is not known. Depending on the discourse relation, we encourage the two events’ polarities to be the same (CA) or reversed (CO). Details are given in Section 3.2."
    #                 "\nC: Results for small labeled training data. Given the performance with the full dataset, we show BERT trained only with the AL data."
    #                 "\nD: Performance of various models on the ACP test set."
    #                 "\nThe output is A or B or C or D. "
    # })
    #
    # print(predictions)
    # print(predictions['answer'])
    # output:
    # {'score': 0.8730505704879761, 'start': 23, 'end': 39, 'answer': 'February 7, 2016'}

    # TODO Dis bert pipeline
    # from transformers import pipeline
    # question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
    #
    # context = "Here is a description of an image: As illustrated in Figure FIGREF1, our key idea is that we can exploit discourse relations BIBREF4 to efficiently propagate polarity from seed predicates that directly report one's emotions (e.g., “to be glad” is positive).",
    # question = "Based on the provided description in the context, please select the most suitable option as a caption for this image. Here are the options:"
    # "\n0: Examples of polarity scores predicted by the BiGRU model trained with AL+CA+CO."
    # "\n1: An overview of our method. We focus on pairs of events, the former events and the latter events, which are connected with a discourse relation, CAUSE or CONCESSION. Dropped pronouns are indicated by brackets in English translations. We divide the event pairs into three types: AL, CA, and CO. In AL, the polarity of a latter event is automatically identified as either positive or negative, according to the seed lexicon (the positive word is colored red and the negative word blue). We propagate the latter event’s polarity to the former event. The same polarity as the latter event is used for the discourse relation CAUSE, and the reversed polarity for CONCESSION. In CA and CO, the latter event’s polarity is not known. Depending on the discourse relation, we encourage the two events’ polarities to be the same (CA) or reversed (CO). Details are given in Section 3.2."
    # "\n2: Results for small labeled training data. Given the performance with the full dataset, we show BERT trained only with the AL data."
    # "\n3: Performance of various models on the ACP test set."
    # "\nThe output is 0 or 1 or 2 or 3. "
    # result = question_answerer(question=question, context=context)
    # print(
    #     f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")


    # TODO Dis Bert with torch
    # from transformers import DistilBertTokenizer, DistilBertModel
    # import torch
    # tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')
    # model = DistilBertModel.from_pretrained('distilbert-base-cased-distilled-squad')
    #
    # text = "Here is a description of an image: As illustrated in Figure FIGREF1, our key idea is that we can exploit discourse relations BIBREF4 to efficiently propagate polarity from seed predicates that directly report one's emotions (e.g., “to be glad” is positive).",
    # question = "Based on the provided description in the context, please select the most suitable option as a caption for this image. Here are the options:"
    # "\n0: Examples of polarity scores predicted by the BiGRU model trained with AL+CA+CO."
    # "\n1: An overview of our method. We focus on pairs of events, the former events and the latter events, which are connected with a discourse relation, CAUSE or CONCESSION. Dropped pronouns are indicated by brackets in English translations. We divide the event pairs into three types: AL, CA, and CO. In AL, the polarity of a latter event is automatically identified as either positive or negative, according to the seed lexicon (the positive word is colored red and the negative word blue). We propagate the latter event’s polarity to the former event. The same polarity as the latter event is used for the discourse relation CAUSE, and the reversed polarity for CONCESSION. In CA and CO, the latter event’s polarity is not known. Depending on the discourse relation, we encourage the two events’ polarities to be the same (CA) or reversed (CO). Details are given in Section 3.2."
    # "\n2: Results for small labeled training data. Given the performance with the full dataset, we show BERT trained only with the AL data."
    # "\n3: Performance of various models on the ACP test set."
    # "\nThe output is 0 or 1 or 2 or 3. "
    #
    #
    # inputs = tokenizer(question, text, return_tensors="pt")
    # with torch.no_grad():
    #     outputs = model(**inputs)
    #
    # print(outputs)

    # TODO Dis Bert with tf
    # from transformers import DistilBertTokenizer, TFDistilBertForQuestionAnswering
    # import tensorflow as tf
    #
    # tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")
    # model = TFDistilBertForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad")
    #
    # text = "Here is a description of an image: As illustrated in Figure FIGREF1, our key idea is that we can exploit discourse relations BIBREF4 to efficiently propagate polarity from seed predicates that directly report one's emotions (e.g., “to be glad” is positive).",
    # question = "Based on the provided description in the context, please select the most suitable option as a caption for this image. Here are the options:"
    # "\n0: Examples of polarity scores predicted by the BiGRU model trained with AL+CA+CO."
    # "\n1: An overview of our method. We focus on pairs of events, the former events and the latter events, which are connected with a discourse relation, CAUSE or CONCESSION. Dropped pronouns are indicated by brackets in English translations. We divide the event pairs into three types: AL, CA, and CO. In AL, the polarity of a latter event is automatically identified as either positive or negative, according to the seed lexicon (the positive word is colored red and the negative word blue). We propagate the latter event’s polarity to the former event. The same polarity as the latter event is used for the discourse relation CAUSE, and the reversed polarity for CONCESSION. In CA and CO, the latter event’s polarity is not known. Depending on the discourse relation, we encourage the two events’ polarities to be the same (CA) or reversed (CO). Details are given in Section 3.2."
    # "\n2: Results for small labeled training data. Given the performance with the full dataset, we show BERT trained only with the AL data."
    # "\n3: Performance of various models on the ACP test set."
    # "\nThe output is 0 or 1 or 2 or 3. "
    #
    # inputs = tokenizer(question, text, return_tensors="tf")
    # outputs = model(**inputs)
    #
    # answer_start_index = int(tf.math.argmax(outputs.start_logits, axis=-1)[0])
    # answer_end_index = int(tf.math.argmax(outputs.end_logits, axis=-1)[0])
    #
    # predict_answer_tokens = inputs.input_ids[0, answer_start_index: answer_end_index + 1]
    # print(tokenizer.decode(predict_answer_tokens))

    # TODO chartqa
    # processor = Pix2StructProcessor.from_pretrained('google/matcha-chartqa')
    # model = Pix2StructForConditionalGeneration.from_pretrained('google/matcha-chartqa')
    #
    #     # url = "https://raw.githubusercontent.com/vis-nlp/ChartQA/main/ChartQA%20Dataset/val/png/20294671002019.png"
    # image = Image.open(constants.blank_png_dir)
    # inputs = processor(images=image, text="Here is a description of an image:"
    #                                       "\nAs illustrated in Figure FIGREF1, our key idea is that we can exploit discourse relations BIBREF4 to efficiently propagate polarity from seed predicates that directly report one's emotions (e.g., “to be glad” is positive)."
    #                                       "\nBased on the provided description of an image, please select the most suitable caption. Answer only the identifier(an upper character) of the chosen option. Here are the options:"
    #                                       "\nA. Examples of polarity scores predicted by the BiGRU model trained with AL+CA+CO."
    #                                       "\nB. An overview of our method. We focus on pairs of events, the former events and the latter events, which are connected with a discourse relation, CAUSE or CONCESSION. Dropped pronouns are indicated by brackets in English translations. We divide the event pairs into three types: AL, CA, and CO. In AL, the polarity of a latter event is automatically identified as either positive or negative, according to the seed lexicon (the positive word is colored red and the negative word blue). We propagate the latter event’s polarity to the former event. The same polarity as the latter event is used for the discourse relation CAUSE, and the reversed polarity for CONCESSION. In CA and CO, the latter event’s polarity is not known. Depending on the discourse relation, we encourage the two events’ polarities to be the same (CA) or reversed (CO). Details are given in Section 3.2."
    #                                       "\nC. Results for small labeled training data. Given the performance with the full dataset, we show BERT trained only with the AL data."
    #                                       "\nD. Performance of various models on the ACP test set.",
    #                        return_tensors="pt")
    # inputs = processor(images=image, text="What is the first upper character?", return_tensors="pt")
    # predictions = model.generate(**inputs, max_new_tokens=512)
    # print(processor.decode(predictions[0], skip_special_tokens=True))


def matching_qap_test(articles):
    evaluator = MatchingQAEvaluator(articles)
    evaluator.evaluate()
    print("matching_qap.json output finished")
    # print("%d question answer pairs in general" % gcount)
    # print("%d pairs answered correct with figures" % bcount)
    # print("In comparison, %d pairs answered correct with captions" % ccount)


def evidence_qap_test(articles):
    evaluator = EviQAEvaluator(articles)
    bleu_scores = evaluator.evaluate()
    # qap_count = len(bleu_scores)
    # print("There are %d question pairs and the average score is %f", qap_count, sum(bleu_scores) / qap_count)


def qasper_read_test():
    reader = QasperReader(constants.qasper_json_dir, constants.qasper_png_base_dir)
    return reader.get_articles()
    # print(Figure.get_contexts(Article.get_figures(reader.get_articles()[0])[0]))


def mqag_generate_test():
    generator = MQAGGenerator(qasper_read_test())
    # To test the result of generation
    q = generator.generate()[0]
    print(q.get_question())
    print(q.get_answer())
    print(q.get_figure().get_dir())


def seperate():
    seperator = "-----------------------------"
    print(seperator)


# show some infos about qasper, including
# count of articles
# count of articles with figures detected
# count of articles with evidence about figures
# count of qa pairs related to figures
# count of articles with missing figures in the datasets
def count_and_show(articles):
    # counting phase
    art_count = len(articles)
    fig_art_count = 0
    evi_art_count = 0
    evi_qap_count = 0
    missing_art_count = 0
    missing_fig_count = 0
    for article in articles:
        if len(article.get_figures()) != 0:
            fig_art_count += 1
        if len(article.fig_qaps) != 0:
            evi_art_count += 1
        if article.missing_fig_num != 0:
            missing_art_count += 1
        evi_qap_count += len(article.fig_qaps)
        missing_fig_count += article.missing_fig_num
    print('count of articles:' + str(art_count))
    print('count of articles with figures detected:' + str(fig_art_count))
    print('count of articles with evidence about figures:' + str(evi_art_count))
    print('count of qa pairs related to figures:' + str(evi_qap_count))
    print('count of articles with missing figures in the datasets:' + str(missing_art_count))
    print('count of missing figures in the datasets:' + str(missing_fig_count))


general_test()
# casual demos for redex tests

# test_txt = "FLOAT: 123"
# pattern = 'FLOAT: (.*)'
# print(re.search(pattern, test_txt).group(1))
