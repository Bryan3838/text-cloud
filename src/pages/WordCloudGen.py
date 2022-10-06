import tkinter as tk
from tkinter import ttk
from wordcloud import WordCloud

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.fonts import LARGE_FONT
from src.TextArray import get_dict

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

    def show(self, controller):
        controller.show_frame("WordCloudGen")
        self.update(controller)

    def update(self, controller):
        if self.data_frame:
            return

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
        
        self.data_frame = ttk.Frame(self.body)
        self.data_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.generate_cloud(combined_dict)
                
    def handle_popup(self, popup, controller):
        popup.destroy()
        self.back_to_source_view(controller)

    def back_to_source_view(self, controller):
        page = controller.get_frame("SourceView")
        page.show(controller)

    def refresh_word_cloud(self, controller):
        if self.data_frame:
            self.data_frame = self.data_frame.destroy()
        
        self.update(controller)
        
    def generate_cloud(self, cloud_dict):
        cloud = WordCloud(width=2000, height=1000, background_color = "white",
        max_font_size = 100, max_words = 300, colormap = "plasma").generate_from_frequencies(cloud_dict)
        cloud = WordCloud(width=1920, height=1080, background_color = "white",
            max_font_size = 100, max_words = 300, colormap = "plasma").generate_from_frequencies(cloud_dict)

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