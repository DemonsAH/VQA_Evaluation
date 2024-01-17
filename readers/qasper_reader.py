import json
import os

from readers.article import Article
from readers.figure import Figure


# this file is to read json files for Qasper datasets for generators.
class QasperReader:

    def __init__(self, json_dir, png_base_dir):
        self.articles = []
        self.json_read(json_dir)

    # To read json file and create Article instance
    def json_read(self, json_dir):
        with open(json_dir, 'r') as json_file:
            json_data = json.load(json_file)
            # print(type(json_data)) ->dict
            for article_num in json_data:
                text = json_data[article_num]["full_text"]
                abstract = json_data[article_num]["abstract"]
                figures = json_data[article_num]["figures_and_tables"]
                qas = json_data[article_num]["qas"]
                new_article = Article(figures, abstract, text, article_num, qas)
                self.articles.append(new_article)
                # only the first article for test TODO delete return to read all papers

    def get_articles(self):
        return self.articles



