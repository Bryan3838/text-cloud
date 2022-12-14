import re

class TextArray():

    def __init__(self, text_array):
        self.text_array = text_array

def clean(text_array, stopwords):
    # lowercase elements
    list = [text.lower() for text in text_array]

    # remove invalid words and numbers (List: ["hi!,", "their's...", "123"] => ["hi", "their's", ""])
    list = [re.sub(r"(?!(?<=[a-z])'[a-z])[^\w\s]|[0-9]", ' ', text, flags=re.I) for text in list]

    # remove whitespace, remove empty strings and filter stopwords (List: ["hi", "their's"])
    list = [text.strip() for text in list if text.strip() and (text.strip() not in stopwords)]
    
    return list

def get_dict(text_array):
        counted_dict = {i:text_array.count(i) for i in text_array}
        sorted_dict = sorted(counted_dict.items(), key=lambda item: item[1])
        reversed_dict = reversed(sorted_dict)
        return dict(reversed_dict)