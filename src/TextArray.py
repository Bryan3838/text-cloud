import re

from src.ResourceUtils import resource_path
stopwords_path = resource_path("./wordcloud/stopwords")

stopwords = list(map(str.strip, open(stopwords_path)))

class TextArray():

    def __init__(self, text_array):
        self.text_array = text_array

    def clean(self):
        list = [text.lower() for text in self.text_array] # lowercase elements
        list = [re.sub(r"[0-9]", '', text) for text in list] # remove numbers
        list = [text for text in list if text not in stopwords] # filter stopwords
        list = [text for text in list if re.compile(r"[a-z]").match(text)] # filter non-alpha char words
        return list

def get_dict(text_array):
        counted_dict = {i:text_array.count(i) for i in text_array}
        sorted_dict = sorted(counted_dict.items(), key=lambda item: item[1])
        reversed_dict = reversed(sorted_dict)
        return dict(reversed_dict)