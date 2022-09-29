import tkinter as tk
from tkinter import ttk
import WordCloud
import matplotlib.pyplot as plt
import pandas

from src.fonts import LARGE_FONT
from src.TextArray import TextArray

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
        
    def generateCloud(self, controller):
        page = controller.get_frame("SourceView")
        cloud = WordCloud(background_color="white",width=1000,height=1000,
        max_words=10,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(page.data.items)
        plt.imshow(cloud)