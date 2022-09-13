import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from src.Camera import Camera
from src.fonts import LARGE_FONT

class ImageCapture(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.ui_components = tk.Frame

        self.ui_components.header = ttk.Label(self, text="Image Capture", font=LARGE_FONT)
        self.ui_components.header.pack(side=tk.TOP)

        self.ui_components.options = ttk.Frame(self)
        self.ui_components.options.pack(side=tk.TOP)

        self.ui_components.body = ttk.Frame(self)
        self.ui_components.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ui_components.button1 = ttk.Button(self, text="Take Image",
            command=lambda: self.take_snapshot(controller))
        self.ui_components.button1.pack(in_=self.ui_components.options, side=tk.LEFT, anchor="n")

        self.ui_components.label_frame = ttk.Labelframe(self)
        self.ui_components.label_frame.pack(in_=self.ui_components.body)
        self.ui_components.image_label = ttk.Label(self.ui_components.label_frame)
        self.ui_components.image_label.pack()

        self.enable_camera()

    def update(self):
        ret, frame = self.camera.get_frame()
        if ret:
            photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.image_label.imgtk = photo
            self.image_label.configure(image=photo)
            
        self.camera_process = self.ui_components.image_label.after(30, self.update)
    
    def show(self, controller):
        controller.show_frame("ImageCapture")

    def take_snapshot(self, controller):
        ret, frame = self.camera.get_frame()
        if ret:
            snapshot = ImageTk.PhotoImage(image=Image.fromarray(frame))

            page = controller.get_frame("ImagePreview")
            page.snapshot = snapshot
            page.show(controller)

    def enable_camera(self):
        self.camera = Camera()
        self.update()

    def disable_camera(self):
        self.ui_components.image_label.after_cancel(self.camera_process)
        if self.camera:
            del self.camera
            self.camera = None