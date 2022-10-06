import tkinter as tk
from tkinter import ttk
from wordcloud import WordCloud
from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.fonts import LARGE_FONT
from src.TextArray import get_dict

root = Tk()

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

    def show(self, controller):
        controller.show_frame("WordCloudGen")
        self.update(controller)

    def update(self, controller):
        if self.data_frame:
            self.data_frame.destroy()
        self.data_frame = ttk.Frame(self.body)
        self.data_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        page = controller.get_frame("SourceView")
        combined_dict = {}
        for data in page.data.items():
            (key, file_type, title, image, text) = page.get_data(data)
            for word, count in get_dict(text.clean()).items():
                if word in combined_dict:
                    combined_dict[word] += count
                else:
                    combined_dict[word] = count
        if len(combined_dict) <= 0:
            print("No valid words in Sources. Please try adding a different source.")
            # Handle error
            pass
        print(combined_dict)
        #self.generate_cloud(combined_dict)

        #Button handling
        root.geometry('500x500')
        #placement = 0
        for key, value in combined_dict.items():
            myLabel = Label(root, text = value)
            myButton = Button(root, text = key, command = myLabel.pack)
            myButton.place(x=100, y=75)
            myButton.pack(side=TOP, anchor="w")
            #placement += 5

        # Bar Plot Example
        keys = combined_dict.keys()
        values = combined_dict.values()
        plt.figure(1)
        plt.bar(keys, values)
        plt.show()
                
    def back_to_source_view(self, controller):
        page = controller.get_frame("SourceView")
        page.show(controller)
        
    def generate_cloud(self, cloud_dict):
        cloud_dict = dict(list(cloud_dict.items())[:75])
        cloud = WordCloud(width=1920, height=1080).generate_from_frequencies(cloud_dict)

        plt.figure(1)
        plt.imshow(cloud, interpolation='bilinear')
        plt.axis("off")
        plt.margins(x=0, y=0)

        canvas = FigureCanvasTkAgg(plt.figure(1), self.data_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.data_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    # def dict_buttons(self):
    #     for key, value in combin.items():
    #         myLabel = Label(root, text=value)
    #         myButton = Button(root, text=key, command=myLabel.pack)
    #         myButton.pack()
