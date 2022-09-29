import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from src.FileType import FileType
from src.ImageText import ImageText
from src.Camera import Camera
from src.fonts import LARGE_FONT

class ImageCapture(tk.Frame):

    def __init__(self, parent, controller):
        self.camera_process = None
        self.camera = None
        
        ttk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Image Capture", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.body = ttk.Frame(self)
        self.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button1 = ttk.Button(self, text="Back",
            command=lambda: self.back(controller))
        self.button1.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.button1 = ttk.Button(self, text="Take Image",
            command=lambda: self.take_snapshot(controller))
        self.button1.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.label_frame = ttk.Labelframe(self)
        self.label_frame.pack(in_=self.body)
        self.image_label = ttk.Label(self.label_frame)
        self.image_label.pack()

    def update(self):
        ret, frame = self.camera.get_frame()
        if ret:
            image = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.image_label.imgtk = image
            self.image_label.configure(image=image)
            
        self.camera_process = self.image_label.after(30, self.update)
    
    def show(self, controller):
        if not self.camera:
            self.enable_camera()
        controller.show_frame("ImageCapture")

    def back(self, controller):
        page = controller.get_frame("Navigation")
        page.show(controller)

    def take_snapshot(self, controller):
        ret, frame = self.camera.get_frame()
        if ret:
            image = Image.fromarray(frame)
            image = ImageText(image)

            page = controller.get_frame("SourceView")
            page.add_data(FileType.IMAGE_FILES, "Image Capture", image, image.text_array)
            page.show(controller)

    def enable_camera(self):
        self.camera = Camera()
        self.update()

    def disable_camera(self):
        if self.camera_process:
            self.image_label.after_cancel(self.camera_process)

        if self.camera:
            del self.camera
            self.camera = None
        
    def __del__(self):
        self.disable_camera()