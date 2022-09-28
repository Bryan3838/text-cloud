import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from src.fonts import LARGE_FONT

class ImagePreview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Image Preview", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.body = ttk.Frame(self)
        self.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button1 = ttk.Button(self, text="Retake Image",
            command=lambda: self.retake_image(controller))
        self.button1.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.button2 = ttk.Button(self, text="Next",
            command=lambda: self.next(controller))
        self.button2.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.label_frames = []
        
    def update(self, controller):
        if self.label_frames:
            for frame in self.label_frames:
                frame.destroy()
        self.label_frames = []

        page = controller.get_frame("SourceView")
        image = page.data[max(page.data.keys())]["image"]
        
        label_frame = ttk.Labelframe(self)
        label_frame.pack(in_=self.body)
        self.label_frames.append(label_frame)
        
        image_label = ttk.Label(label_frame)
        image_label.pack()
        imagetk = ImageTk.PhotoImage(image=image)
        image_label.imgtk = imagetk
        image_label.configure(image=imagetk)
            

    def show(self, controller):
        controller.show_frame("ImagePreview")
        self.update(controller)

    def retake_image(self, controller):
        page = controller.get_frame("SourceView")
        del page.data[max(page.data.keys())]

        page = controller.get_frame("ImageCapture")
        page.show(controller)

    def next(self, controller):
        page = controller.get_frame("SourceView")
        page.show(controller)

        page1 = controller.get_frame("ImageCapture")
        page1.disable_camera()