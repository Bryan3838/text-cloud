import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from src.components.ScrollableImage import ScrollableImage
from src.components.ScrollableFrame import ScrollableFrame
from src.ImageText import ImageText

from src.fonts import LARGE_FONT

class TextExtraction(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Text Extraction", font=LARGE_FONT)
        self.header.pack(side=tk.TOP)

        self.options = ttk.Frame(self)
        self.options.pack(side=tk.TOP)

        self.body = ScrollableFrame(self)
        self.body.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.button1 = ttk.Button(self, text="Add Another Source",
            command=lambda: self.add_another_source(controller))
        self.button1.pack(in_=self.options, side=tk.LEFT, anchor="nw")

        self.count = 0
        self.data = {}
        self.data_frames = []

    def show(self, controller):
        controller.show_frame("TextExtraction")
        self.update(controller)

    def add_another_source(self, controller):
        page = controller.get_frame("Navigation")
        page.show(controller)

    def update(self, controller):
        if self.data_frames:
            for frame in self.data_frames:
                if frame:
                    frame.destroy()
        self.data_frames = []

        if self.data:
            for data in self.data.items():
                key = data[0]
                title = data[1]["title"]
                image = data[1]["image"]
                text = data[1]["text"]

                data_frame = ttk.Frame(self.body.scrollable_frame)
                data_frame.pack(side=tk.TOP)
                self.data_frames.append(data_frame)

                text_label = ttk.Label(data_frame, text=title, font=LARGE_FONT)
                text_label.pack(side=tk.TOP)
                self.data_frames.append(text_label)

                if image:
                    processed_image = image.get_text_bounding_box_image()
                    imagetk = ImageTk.PhotoImage(image=processed_image)

                    image_window = ScrollableImage(data_frame, image=imagetk, scrollbarwidth=12, width=1080, height=720)
                    image_window.pack(side=tk.TOP)
                    self.data_frames.append(image_window)

                if text:
                    text_box = tk.Text(data_frame)
                    text_box.insert(tk.END, " ".join(text.text_array))
                    text_box.pack(side=tk.TOP)
                    self.data_frames.append(text_box)


                button_delete = ttk.Button(data_frame, text="Delete",
                    command=lambda frame=data_frame, key=key: self.delete_data(frame, key))
                button_delete.pack(side=tk.TOP)

    def add_data(self, title, image, text_array):
        self.data.update({
            self.count: {
                "title": title,
                "image": image,
                "text": text_array,
            }
        })
        self.count += 1

    def delete_data(self, frame, key):
        frame.destroy()
        del self.data[key]
        
