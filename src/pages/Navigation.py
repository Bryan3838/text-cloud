import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image
import PyPDF2

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
        self.file_paths = None

        ttk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Navigation", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.button1 = ttk.Button(self.options, text="Open Camera",
            command=lambda: self.open_camera(controller))
        self.button1.pack(side=tk.TOP)

        self.button2 = ttk.Button(self.options, text="Upload File",
            command=lambda: self.upload_files(controller))
        self.button2.pack(side=tk.TOP)

        self.button3 =  ttk.Button(self.options, text="Insert Text",
            command=lambda: self.insert_text(controller))
        self.button3.pack(side=tk.TOP)

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

            title = base_name
            image = None
            text = None
            if category == FileType.IMAGE_FILES:
                image = Image.open(path)
                image = ImageText(image)

                text = image.text_array
            elif category == FileType.TEXT_FILES:
                text_read = []
                with open(path) as f:
                    for line in f:
                        text_read.append(line.strip())
                text = TextArray(text_read)

            elif category == FileType.PDF_FILE:
                text_read = []
                pdf_obj = open(path, "rb")
                pdf_reader = PyPDF2.PdfFileReader(pdf_obj)
                for i in range(pdf_reader.numPages):
                    page_obj = pdf_reader.getPage(i)
                    text_read.append(page_obj.extract_text())
                text = TextArray(text_read)

            page.add_data(category, title, image, text)

        page1 = controller.get_frame("SourceView")
        page1.show(controller)

    def insert_text(self, controller):
        page = controller.get_frame("SourceView")
        page.add_data(FileType.TEXT_FILES, "Text Input", None, TextArray([]))
        
        page1 = controller.get_frame("SourceView")
        page1.show(controller)