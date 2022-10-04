import re
import nltk
from nltk.corpus import stopwords
import csv

nltk.download('stopwords', quiet=True)

class TextArray():

    def __init__(self, text_array):
        self.text_array = text_array

    def get_dict(self):
        counted_dict = {i:self.text_array.count(i) for i in self.text_array}
        sorted_dict = sorted(counted_dict.items(), key=lambda item: item[1])
        reversed_dict = reversed(sorted_dict)
        return dict(reversed_dict)

    def clean(self):
        list = [text.lower() for text in self.text_array] # lowercase elements
        list = [re.sub("[0-9]", '', text) for text in list] # filter numbers
        list = [text for text in list if text not in stopwords.words('english')] # filter stopwords
        text = " ".join(list)
        text = re.findall(r"\w+", text)
        return text



