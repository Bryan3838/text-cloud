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

from src.components.ScrollableFrame import ScrollableFrame
from src.fonts import LARGE_FONT
from src.TextArray import get_dict, clean
from src.ResourceUtils import resource_path

stopwords_path = resource_path("./wordcloud/stopwords")
image_font_path = resource_path("./wordcloud/DroidSansMono.ttf")

stopwords = list(map(str.strip, open(stopwords_path)))

MAX_WORDS = 300
MAX_FONT_SIZE = 200

class WordCloudGen(tk.Frame):
    
    def __init__(self, parent, controller):
        self.data_frame = None

        tk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Word Cloud", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.button1 = ttk.Button(self.options, text="Back to Source View",
            command=lambda: self.back_to_source_view(controller))
        self.button1.pack(side=tk.LEFT, anchor="n")

        self.button2 = ttk.Button(self.options, text="Regenerate",
            command=lambda: self.refresh_word_cloud(controller))
        self.button2.pack(side=tk.LEFT, anchor="n")

        self.body = ScrollableFrame(self)
        self.body.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.data_frame = ttk.Frame(self.body.scrollable_frame)
        self.data_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.fig1 = Figure(dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig1, self.data_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        NavigationToolbar2Tk(self.canvas, self.data_frame)
        self.canvas.get_tk_widget().pack()

        self.label = ttk.Label(self.body.scrollable_frame, text="Stopwords", font=LARGE_FONT)
        self.label.pack(side=tk.TOP)

        text_box = tk.Text(self.body.scrollable_frame)
        text_box.insert(tk.END, ",".join(stopwords))
        text_box.pack(side=tk.TOP, fill=tk.X, expand=True)
        button_update = ttk.Button(self.body.scrollable_frame, text="Update",
            command=lambda text_box=text_box: self.update_text(text_box))
        button_update.pack(side=tk.TOP)

    def show(self, controller):
        controller.show_frame("WordCloudGen")
        self.update(controller)

    def update(self, controller):
        page = controller.get_frame("SourceView")
        combined_dict = {}
        for data in page.data.items():
            (key, file_type, title, image, text) = page.get_data(data)
            for word, count in get_dict(clean(text.text_array, stopwords)).items():
                if word in combined_dict:
                    combined_dict[word] += count
                else:
                    combined_dict[word] = count
        combined_dict = dict(reversed(sorted(combined_dict.items(), key=lambda item: item[1])))

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
        class MyColorFunctor():
            def __init__(self,frequencies):
                self.frequencies = frequencies

            def __call__(self,word,font_size,position,orientation,random_state=None,**kwargs):
                hsl_color = "hsl(%d, 80%%, 50%%)" % ((360-60) * (font_size/200)) #(360/(1+360*math.exp(self.frequencies[word])/(self.max/10))) ## Sigmoid
                return hsl_color
        
        cloud = WordCloud(width=1920, height=1080, background_color="white",
            max_font_size=MAX_FONT_SIZE, max_words=MAX_WORDS,  color_func=MyColorFunctor(cloud_dict), font_path=image_font_path).generate_from_frequencies(cloud_dict)

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
        plt.xlabel("Words")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(np.arange(0, max(values) + 1, math.ceil((max(values) / 10)) + 1))
        plt.show()

    def update_text(self, text_box):
        global stopwords
        stopwords = list(text_box.get("1.0","end-1c").replace(" ", "").split(","))

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