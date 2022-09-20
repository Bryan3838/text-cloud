import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.spacer_frame = tk.Frame(self, width=20)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.frame_size)
        self.canvas.bind_class(self.canvas, "<MouseWheel>", self.mouse_scroll)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.spacer_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            self.canvas.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.canvas.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

    def frame_size(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))