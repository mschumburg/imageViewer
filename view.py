import tkinter as Tk
from PIL import Image, ImageTk

from timer import Timer

class View:
    t = Timer()
    def __init__(self, root, model):
        self.frame = Tk.Frame(root)
        self.model = model
        self.frame.pack()

        root.bind('<Right>', self.next)
        root.bind('<Left>', self.prev)

        
        self.t.start()
        rawImage = model.getAtIndexImg(0)
        
        rawImage = ImageTk.PhotoImage(rawImage)
        
        self.test = Tk.Label(self.frame, image=rawImage, width=1280, height=720)
        self.test.image = rawImage
        self.test.pack()
        self.t.stop()

    def next(self, e):
        self.t.start()
        rawImage = self.model.getNextImg()
        rawImage = ImageTk.PhotoImage(rawImage)
        self.test.configure(image=rawImage)
        self.test.image = rawImage
        self.t.stop()

    def prev(self, e):
        rawImage = self.model.getPrevImg()
        rawImage = ImageTk.PhotoImage(rawImage)
        self.test.configure(image=rawImage)
        self.test.image = rawImage


