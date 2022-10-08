import re

class TextArray():

    def __init__(self, text_array):
        self.text_array = text_array

def clean(text_array, stopwords):
    list = [text.lower() for text in text_array] # lowercase elements
    list = [re.sub(r"[0-9]", '', text) for text in list] # remove numbers
    list = [re.sub(r"(?!(?<=[a-z])'[a-z])[^\w\s]", ' ', text, flags=re.I) for text in list] # remove non-puncuated words
    list = [text.strip() for text in list] # remove whitespace
    list = [text for text in list if text not in stopwords] # filter stopwords
    return list

def get_dict(text_array):
        counted_dict = {i:text_array.count(i) for i in text_array}
        sorted_dict = sorted(counted_dict.items(), key=lambda item: item[1])
        reversed_dict = reversed(sorted_dict)
        return dict(reversed_dict)