import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from src.ImageText import ImageText
from src.Camera import Camera
from src.fonts import LARGE_FONT

class ImageCapture(tk.Frame):
    #basically sets up the window for the app with labels for buttons and navigation
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        #Window lable for Image Capture Window
        self.header = ttk.Label(self, text="Image Capture", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.body = ttk.Frame(self)
        self.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #Navigation Button for taking an Image using a webcam
        self.button1 = ttk.Button(self, text="Take Image",
            command=lambda: self.take_snapshot(controller))
        self.button1.pack(in_=self.options, side=tk.LEFT, anchor="n")

        self.label_frame = ttk.Labelframe(self)
        self.label_frame.pack(in_=self.body)
        self.image_label = ttk.Label(self.label_frame)
        self.image_label.pack()

        self.camera_process = None
        self.camera = None
    #gets frames from the webcam and stores them into an image array at a speed of 30 ms
    def update(self):
        ret, frame = self.camera.get_frame()
        if ret:
            image = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.image_label.imgtk = image
            self.image_label.configure(image=image)
            
        self.camera_process = self.image_label.after(30, self.update)
    #turns on the camera on the starting of the app
    def show(self, controller):
        if not self.camera:
            self.enable_camera()
        controller.show_frame("ImageCapture")
    #takes the capture image of the camera; checks if its in the array and returns the specific frame
    def take_snapshot(self, controller):
        ret, frame = self.camera.get_frame()
        if ret:
            image = Image.fromarray(frame)
            image = ImageText(image)

            page = controller.get_frame("SourceView")
            page.add_data("Image Capture", image, image.text_array)
            page.show(controller)
    #turns on camera
    def enable_camera(self):
        self.camera = Camera()
        self.update()
    #turns off camera after closing window
    def disable_camera(self):
        if self.camera_process:
            self.image_label.after_cancel(self.camera_process)

        if self.camera:
            del self.camera
            self.camera = None
