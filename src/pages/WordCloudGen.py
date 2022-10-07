import tkinter as tk
from tkinter import ttk

import numpy as np
import math
from wordcloud import WordCloud

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.fonts import LARGE_FONT
from src.TextArray import get_dict

# stopwords = ["where's", 'having', 'under', "weren't", 'cannot', 'nor', 'where', 'same', 'of', 'should', "shouldn't", 'or', 'than', 'once', 'therefore', 'yourselves', 'does', 'those', 'be', 'below', 'only', 'into', "they'll", "she'd", 'com', 'at', "wouldn't", "that's", 'this', "here's", "i've", "let's", 'however', 'r', 'its', 'was', "isn't", 'am', 'http', "she's", 'again', 'been', 'hence', "she'll", 'all', "wasn't", 'between', 'what', "can't", "haven't", 'theirs', 'how', 'there', 'no', 'who', 'they', 'own', 'such', 'with', 'by', 'to', 'get', "what's", "they've", 'why', 'you', "i'd", 'k', "don't", 'most', 'over', 'but', 'and', 'through', 'from', 'do', 'which', 'during', 'he', 'a', "when's", 'shall', 'my', 'i', 'both', "they're", "aren't", 'in', 'before', 'itself', "we're", 'that', 'your', "we'll", 'each', 'would', 'as', 'them', 'then', 'ours', 'ought', 'hers', 'him', 'an', 'are', "he's", 'too', 'against', 'for', 'these', 'when', "you'll", 'themselves', "who's", 'after', 'more', 'on', 'whom', 'did', 'yours', 'above', 'other', 'his', 'since', 'up', 'had', 'very', "you've", 'also', 'have', 'doing', "we'd", 'any', "i'm", "couldn't", "he'll", "he'd", "hadn't", 'otherwise', 'the', "we've", 'else', 'while', 'yourself', "mustn't", 'being', "doesn't", 'out', "they'd", 'www', 'down', 'about', 'just', 'she', 'if', 'so', "there's", 'has', "why's", 'could', 'were', "won't", 'off', 'me', 'some', 'like', "shan't", 'himself', 'few', 'myself', "hasn't", "didn't", 'her', 'we', 'herself', 'further', 'their', 'until', 'here', 'is', "you'd", 'ever', "it's", "how's", 'our', 'because', 'can', "i'll", 'ourselves', 'it', 'not', "you're"]

class WordCloudGen(tk.Frame):
    
    def __init__(self, parent, controller):
        self.data_frame = None

        tk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Word Cloud", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.body = ttk.Frame(self)
        self.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button1 = ttk.Button(self, text="Back to Source View",
            command=lambda: self.back_to_source_view(controller))
        self.button1.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.button2 = ttk.Button(self, text="Regenerate",
            command=lambda: self.refresh_word_cloud(controller))
        self.button2.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.fig1 = Figure(dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig1, self.body)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        NavigationToolbar2Tk(self.canvas, self.body)
        self.canvas.get_tk_widget().pack()

    def show(self, controller):
        controller.show_frame("WordCloudGen")
        self.update(controller)

    def update(self, controller):
        page = controller.get_frame("SourceView")
        combined_dict = {}
        for data in page.data.items():
            (key, file_type, title, image, text) = page.get_data(data)
            for word, count in get_dict(text.clean()).items():
                if word in combined_dict:
                    combined_dict[word] += count
                else:
                    combined_dict[word] = count
        
        print(combined_dict)

        if len(combined_dict) <= 0:
            popup = tk.Toplevel(self)
            popup.wm_title("Error")
            popup.tkraise(self)
            tk.Label(popup, text="No valid words in Sources. Please try adding a different source.").pack(side=tk.TOP, fill=tk.X, pady=10)
            tk.Button(popup, text="Okay",
                command=lambda: self.handle_popup(popup, controller)).pack()
            center(popup)
            return

        self.generate_cloud(combined_dict)
                
    def handle_popup(self, popup, controller):
        popup.destroy()
        self.back_to_source_view(controller)

    def back_to_source_view(self, controller):
        page = controller.get_frame("SourceView")
        page.show(controller)

    def refresh_word_cloud(self, controller):
        self.update(controller)
        
    def generate_cloud(self, cloud_dict):
        cloud = WordCloud(width=1920, height=1080, background_color = "white",
            max_font_size = 100, max_words = 300, colormap = "plasma").generate_from_frequencies(cloud_dict)

        self.plot = self.fig1.add_subplot(111)
        self.plot.imshow(cloud, interpolation='bilinear')
        self.plot.axis("off")
        self.plot.margins(x=0, y=0)

        self.canvas.draw()

        limit_dict = dict(list(cloud_dict.items())[:25])
        keys = limit_dict.keys()
        values = limit_dict.values()
        plt.figure(1)
        plt.bar(keys, values)
        plt.xlabel("Word")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(np.arange(0, max(values) + 1, math.ceil((max(values) / 10)) + 1))
        plt.show()

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frame_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frame_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frame_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()