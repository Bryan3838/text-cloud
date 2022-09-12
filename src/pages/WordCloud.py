import tkinter as tk
from tkinter import ttk

from src.fonts import LARGE_FONT

class WordCloud(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ui_components = tk.Frame

        self.ui_components.label = ttk.Label(self, text="Word Cloud", font=LARGE_FONT)
        self.ui_components.label.pack(pady=10, padx=10)

        self.ui_components.button1 = ttk.Button(self, text="Scan Another Image",
            command=lambda: self.scan_another_image(controller))
        self.ui_components.button1.pack()
    
    def show(self, controller):
        controller.show_frame("WordCloud")

    def scan_another_image(self, controller):
        page = controller.get_frame("ImageCapture")
        page.enable_camera()
        page.show(controller)