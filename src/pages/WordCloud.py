import tkinter as tk
from tkinter import ttk

from src.fonts import LARGE_FONT

class WordCloud(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Word Cloud", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

    def show(self, controller):
        controller.show_frame("WordCloud")
        self.update(controller)

    def update(self, controller):
        page = controller.get_frame("SourceView")
        print(page.data)
        for data in page.data.items():
            (key, file_type, title, image, text) = page.get_data(data)
            