import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from src.FileType import FileType
from src.TextArray import TextArray
from src.components.ScrollableImage import ScrollableImage
from src.components.ScrollableFrame import ScrollableFrame

from src.fonts import LARGE_FONT, MEDIUM_FONT

class SourceView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.header = ttk.Label(self, text="Source View", font=LARGE_FONT)
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
        controller.show_frame("SourceView")
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
                file_type = data[1]["file_type"]
                title = data[1]["title"]
                image = data[1]["image"]
                text = data[1]["text"]

                data_frame = ttk.Frame(self.body.scrollable_frame)
                data_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
                self.data_frames.append(data_frame)

                text_label = ttk.Label(data_frame, text=title, font=LARGE_FONT)
                text_label.pack(side=tk.TOP)
                self.data_frames.append(text_label)

                if image:
                    processed_image = image.get_text_bounding_box_image()
                    imagetk = ImageTk.PhotoImage(image=processed_image)

                    image_window = ScrollableImage(data_frame, image=imagetk, scrollbarwidth=12, width=1080, height=min(imagetk.height(), 780))
                    image_window.pack(side=tk.TOP, fill=tk.X, expand=True)
                    self.data_frames.append(image_window)

                if text:
                    if len(text.text_array) == 0 and not file_type == FileType.TEXT_FILES:
                        text_box_text_label = tk.Label(data_frame, text="No text found.", font=MEDIUM_FONT, fg="red")
                        text_box_text_label.pack(side=tk.TOP)
                        self.data_frames.append(text_box_text_label)
                    else:
                        text_box = tk.Text(data_frame)
                        text_box.insert(tk.END, " ".join(text.text_array))
                        text_box.pack(side=tk.TOP, fill=tk.X, expand=True)
                        self.data_frames.append(text_box)
                        button_update = ttk.Button(data_frame, text="Update",
                            command=lambda key=key, text_box=text_box: self.update_text(key, text_box))
                        button_update.pack(side=tk.TOP)

                button_delete = ttk.Button(data_frame, text="Delete",
                    command=lambda frame=data_frame, key=key: self.delete_data(frame, key))
                button_delete.pack(side=tk.TOP)

                separator_frame = tk.Frame(self.body.scrollable_frame, height=10, bg="gray")
                separator_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

    def add_data(self, file_type, title, image, text):
        self.data.update({
            self.count: {
                "file_type": file_type,
                "title": title,
                "image": image,
                "text": text,
            }
        })
        self.count += 1

    def update_text(self, key, text_box):
        text = TextArray(text_box.get("1.0","end-1c").split())
        data = self.data[key]
        self.data.update({
            key: {
                "file_type": data["file_type"],
                "title": data["title"],
                "image": data["image"],
                "text": text,
            }
        })

    def delete_data(self, frame, key):
        frame.destroy()
        del self.data[key]
        
