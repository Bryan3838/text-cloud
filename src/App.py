import tkinter as tk
import sys

from src.pages.ImageCapture import ImageCapture
from src.pages.ImagePreview import ImagePreview
from src.pages.WordCloud import WordCloud

pages = {
    "ImageCapture": ImageCapture,
    "ImagePreview": ImagePreview,
    "WordCloud": WordCloud
}

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        def on_closing():
            page = self.get_frame("ImageCapture")
            page.disable_camera()

            sys.exit()

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "App")

        self.protocol("WM_DELETE_WINDOW", on_closing)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Exit", command=on_closing)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for V, F in pages.items():
            frame = F(container, self)
            self.frames[V] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ImageCapture")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_frame(self, page_name):
        return self.frames[page_name]

app = App()
app.geometry("1280x720")
app.mainloop()