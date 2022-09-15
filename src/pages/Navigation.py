import os
import numpy as np
import tkinter as tk
import re
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image
from src.ImageText import ImageText

from src.FileType import file_types_list, FileType
from src.TextArray import TextArray

from src.fonts import LARGE_FONT

def get_file_category_from_extension(file_extension):
    for file_category in file_types_list:
        category, file_types = file_category
        for suffix in file_types:
            extension = suffix[1:]
            if file_extension == extension:
                return FileType(category)
    return None

def handle_image(file_path):
    return Image.open(file_path)

def open_files():
    file_paths = fd.askopenfilenames(
        title='Open files',
        initialdir='/',
        filetypes=file_types_list
    )
    return file_paths

class Navigation(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Navigation", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.button1 = ttk.Button(self, text="Open Camera",
            command=lambda: self.open_camera(controller))
        self.button1.pack(in_=self.options)

        self.button2 = ttk.Button(self, text="Upload File",
            command=lambda: self.upload_files(controller))
        self.button2.pack(in_=self.options)

        self.button3 =  ttk.Button(self, text="Insert Text",
            command=lambda: self.insert_text(controller))
        self.button3.pack(in_=self.options)

        self.file_paths = None

    def show(self, controller):
        controller.show_frame("Navigation")

    def open_camera(self, controller):
        page = controller.get_frame("ImageCapture")
        page.show(controller)

    def upload_files(self, controller):
        self.file_paths = open_files()
        if not self.file_paths:
            return
            
        for path in self.file_paths:
            base_name = os.path.basename(path)
            prefix, suffix = os.path.splitext(base_name)
            extension = suffix[1:]
            category = get_file_category_from_extension(extension)

            page = controller.get_frame("SourceView")

            if category == FileType.IMAGE_FILES:
                image = Image.open(path)
                image = ImageText(image)

                page.add_data(base_name, image, image.text_array)
            elif category == FileType.TEXT_FILES:
                text = []
                with open(path) as f:
                    for line in f:
                        text.append(line.strip())
                text_array = TextArray(text)

                page.add_data(base_name, None, text_array)
            elif category == FileType.PDF_FILE:
                pass
        page1 = controller.get_frame("SourceView")
        page1.show(controller)

    def insert_text(self, controller):
        page = controller.get_frame("SourceView")
        page.add_data("Text Input", None, TextArray([]))
        
        page1 = controller.get_frame("SourceView")
        page1.show(controller)