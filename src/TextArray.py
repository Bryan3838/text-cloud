import re

class TextArray():

    def __init__(self, text_array):
        self.text_array = self.cleaned(text_array)

    def get_dict(self):
        counted_dict = {i:self.text_array.count(i) for i in self.text_array}
        sorted_dict = sorted(counted_dict.items(), key=lambda item: item[1])
        reversed_dict = reversed(sorted_dict)
        return dict(reversed_dict)

    def cleaned(self, text_array):
        list = [re.sub("[0-9]", '', i) for i in text_array]
        text = " ".join(list)
        return re.findall(r"\w+", text.lower())