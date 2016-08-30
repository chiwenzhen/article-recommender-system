# coding=utf-8
import pickle


class Article:
    def __init__(self, a_title, a_text, a_url, a_time, a_tags, a_category=None, a_author=None):
        self.a_title = a_title
        self.a_text = a_text
        self.a_author = a_author
        self.a_url = a_url
        self.a_time = a_time
        self.a_tags = a_tags
        self.a_category = a_category


class ArticleDumper:
    def __init__(self):
        pass

    @staticmethod
    def dump(obj, file_name):
        pickle.dump(obj, open(file_name, "wb"), True)

    @staticmethod
    def load(file_name):
        obj = pickle.load(open(file_name, "rb"))
        return obj



