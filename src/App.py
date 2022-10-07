import tkinter as tk
import sys

from src.pages.Navigation import Navigation
from src.pages.ImageCapture import ImageCapture
from src.pages.ImagePreview import ImagePreview
from src.pages.SourceView import SourceView
from src.pages.WordCloudGen import WordCloudGen

pages = {
    "Navigation": Navigation,
    "ImageCapture": ImageCapture,
    "ImagePreview": ImagePreview,
    "SourceView": SourceView,
    "WordCloudGen": WordCloudGen,
}

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "App")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for V, F in pages.items():
            frame = F(container, self)
            self.frames[V] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Navigation")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_frame(self, page_name):
        return self.frames[page_name]

    def on_closing(self):
        sys.exit()