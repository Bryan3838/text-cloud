import tkinter as tk
from tkinter import ttk
import pytesseract
from pytesseract import Output
import cv2
import numpy
import time

from PIL import Image, ImageTk

from src.fonts import LARGE_FONT

myconfig = r"--psm 11 --oem 3"

class WordCloud(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ui_components = tk.Frame

        self.ui_components.header = ttk.Label(self, text="Image Capture", font=LARGE_FONT)
        self.ui_components.header.pack(side=tk.TOP)

        self.ui_components.options = ttk.Frame(self)
        self.ui_components.options.pack(side=tk.TOP)

        self.ui_components.body = ttk.Frame(self)
        self.ui_components.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ui_components.button1 = ttk.Button(self, text="Scan Another Image",
            command=lambda: self.scan_another_image(controller))
        self.ui_components.button1.pack(in_=self.ui_components.options, side=tk.LEFT, anchor="n")

        label_frame = ttk.Labelframe(self)
        label_frame.pack(in_=self.ui_components.body)
        self.image_label = ttk.Label(label_frame)
        self.image_label.pack()
    
    def show(self, controller):
        controller.show_frame("WordCloud")
        self.update(controller)

    def scan_another_image(self, controller):
        page = controller.get_frame("ImageCapture")
        page.enable_camera()
        page.show(controller)

    def update(self, controller):
        page = controller.get_frame("ImagePreview")
        image = ImageTk.getimage(page.snapshot)
        width, height = image.size

        data = pytesseract.image_to_data(image, config=myconfig, output_type=Output.DICT)
        amount_boxes = len(data['text'])

        image = numpy.array(image)
        for i in range(amount_boxes):
            if float(data['conf'][i]) > 50:
                (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                image = cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
                image = cv2.putText(image, data['text'][i], (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # boxes = pytesseract.image_to_boxes(image, config=myconfig)
        # for box in boxes.splitlines():
        #     box = box.split(" ")
        #     image = cv2.rectangle(numpy.array(image), (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])), (0, 255, 0), 2)

        photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.image_label.imgtk = photo
        self.image_label.configure(image=photo)
        
