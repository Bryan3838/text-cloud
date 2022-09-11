import tkinter as tk
from tkinter import ttk
import sys
from PIL import Image, ImageTk
from Camera import Camera

LARGE_FONT = ("Verdana", 12)

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "App")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Exit", command=sys.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (ImageCapture, ImagePreview, WordCloud):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ImageCapture)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_frame(self, cont):
        return self.frames[cont]

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
        controller.show_frame(ImageCapture)

    def take_snapshot(self, controller):
        ret, frame = self.camera.get_frame()
        snapshot = ImageTk.PhotoImage(image = Image.fromarray(frame))

        page = controller.get_frame(ImagePreview)
        page.snapshot = snapshot
        page.show(controller)

    def enable_camera(self):
        self.camera = Camera()
        self.update()

    def disable_camera(self):
        self.ui_components.image_label.after_cancel(self.camera_process)
        del self.camera

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
        controller.show_frame(ImagePreview)

    def retake_image(self, controller):
        startPage = controller.get_frame(ImageCapture)
        startPage.show(controller)

    def next(self, controller):
        page = controller.get_frame(WordCloud)
        page.show(controller)

        page1 = controller.get_frame(ImageCapture)
        page1.disable_camera()

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
        controller.show_frame(WordCloud)

    def scan_another_image(self, controller):
        page = controller.get_frame(ImageCapture)
        page.enable_camera()
        page.show(controller)

app = App()
app.geometry("1280x720")
app.mainloop()