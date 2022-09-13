import tkinter as tk
from tkinter import ttk

from src.fonts import LARGE_FONT

class ImagePreview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ui_components = tk.Frame

        self.ui_components.header = ttk.Label(self, text="Image Capture", font=LARGE_FONT)
        self.ui_components.header.pack(side=tk.TOP)

        self.ui_components.options = ttk.Frame(self)
        self.ui_components.options.pack(side=tk.TOP)

        self.ui_components.body = ttk.Frame(self)
        self.ui_components.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ui_components.button1 = ttk.Button(self, text="Retake Image",
            command=lambda: self.retake_image(controller))
        self.ui_components.button1.pack(in_=self.ui_components.options, side=tk.LEFT, anchor="n")

        self.ui_components.button2 = ttk.Button(self, text="Next",
            command=lambda: self.next(controller))
        self.ui_components.button2.pack(in_=self.ui_components.options, side=tk.LEFT, anchor="n")

        label_frame = ttk.Labelframe(self)
        label_frame.pack(in_=self.ui_components.body)
        self.image_label = ttk.Label(label_frame)
        self.image_label.pack()
        
    def update(self):
        if self.snapshot:
            self.image_label.imgtk = self.snapshot
            self.image_label.configure(image=self.snapshot)

    def show(self, controller):
        self.update()
        controller.show_frame("ImagePreview")

    def retake_image(self, controller):
        page = controller.get_frame("ImageCapture")
        page.show(controller)

    def next(self, controller):
        page = controller.get_frame("WordCloud")
        page.show(controller)

        page1 = controller.get_frame("ImageCapture")
        page1.disable_camera()