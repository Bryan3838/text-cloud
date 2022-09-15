import pytesseract
from pytesseract import Output
import cv2
import numpy
from PIL import Image

from src.TextArray import TextArray

myconfig = r"--psm 11 --oem 3"

class ImageText():

    def __init__(self, image):
        self.image = image
        self.data = pytesseract.image_to_data(self.image, config=myconfig, output_type=Output.DICT)
        self.text_array = self.get_text_array()

    def get_text_bounding_box_image(self):
        amount_boxes = len(self.data["text"])

        width, height = self.image.size
        image = numpy.array(self.image)
        for i in range(amount_boxes):
            if float(self.data["conf"][i]) > 50:
                (x, y, width, height) = (self.data["left"][i], self.data["top"][i], self.data["width"][i], self.data["height"][i])
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                image = cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
                image = cv2.putText(image, self.data["text"][i], (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return Image.fromarray(image)

    def get_text_array(self):
        amount_boxes = len(self.data["text"])
        valid_text = []

        for i in range(amount_boxes):
            if float(self.data["conf"][i]) > 50:
                valid_text.append(self.data["text"][i])

        return TextArray(valid_text)
