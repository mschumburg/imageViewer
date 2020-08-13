from tkinter import *
import glob
# pip install pillow
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import time

import rawpy

from pathlib import Path

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.iv = iv
        self.master = master
        self.pack()

        # path = './DSCF8807.RAF'
        # rgb = None
        # with rawpy.imread(path) as raw:
        #     rgb = raw.postprocess(no_auto_bright=True, half_size=True)

        # rawImage = Image.fromarray(rgb)

        # width = rawImage.width
        # height = rawImage.height
        # ratio = min(1280/width, 720/height)
        # newWidth = int(width * ratio)
        # newHeight = int(height * ratio)
        # print(ratio)
        # rawImage = rawImage.resize((newWidth, newHeight))

        # rawRender = ImageTk.PhotoImage(rawImage)
        # print('3')


        #self.imgLabel = Label(self, image=rawRender, width=1280, height=720)
        #self.imgLabel.image = rawRender
        self.imgLabel = Label(self, text='rawRender')
        self.imgLabel.pack()

        b1 = Button(self, text='lol', command=self.fwd)
        b1.pack()

    def set_imageViewer(self, iv):
        self.iv = iv

    def fwd(self):
        start = time.time()
        rawImage = self.iv.get_next()
        rawRender = ImageTk.PhotoImage(rawImage)
        self.imgLabel.configure(image=rawRender, width=1280, height=720)
        self.imgLabel.image = rawRender
        end = time.time()
        print(end - start)

    def fwd2(self):
        #path = './img/DSCF8805.RAF'
        
        path = self.iv.get_next()
        print(path)

        rgb = None
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess(no_auto_bright=True, half_size=True)
        rawImage = Image.fromarray(rgb)

        width = rawImage.width
        height = rawImage.height
        ratio = min(1280/width, 720/height)
        newWidth = int(width * ratio)
        newHeight = int(height * ratio)

        rawImage = rawImage.resize((newWidth, newHeight))

        rawRender = ImageTk.PhotoImage(rawImage)

        self.imgLabel.configure(image=rawRender, width=1280, height=720)
        self.imgLabel.image = rawRender
        

class ImageViewer():
    imgList = []
    index = -1
    prerenderCount = 3
    prerenderList = []
    prerenderListIndex = []

    d = {}

    def __init__(self):
        for img in glob.glob('./img/*.RAF'):
            self.imgList.append(img)
            print(img)
        
        self.prerender()

    def prerender(self):
        cin = 0
        if self.index != -1:
            cin = self.index

        for i, imgPath in enumerate(self.imgList, start=cin):
            rgb = None
            with rawpy.imread(imgPath) as raw:
                rgb = raw.postprocess(no_auto_bright=True, half_size=True)
            rawImage = Image.fromarray(rgb)

            width = rawImage.width
            height = rawImage.height
            ratio = min(1280/width, 720/height)
            newWidth = int(width * ratio)
            newHeight = int(height * ratio)

            rawImage = rawImage.resize((newWidth, newHeight))

            #rawRender = ImageTk.PhotoImage(rawImage)

            self.prerenderList.append(rawImage)
            #self.prerenderList.append(cin)
            self.d[cin] = len(self.prerenderList) - 1

            if i == (self.prerenderCount + cin):
                print(i)
                break

    def get_next(self):
        if self.index < 0:
            self.index = 0
            # return self.imgList[0]
            return self.prerenderList[0]

        else:
            self.index += 1
            return self.prerenderList[self.index]
            #return self.imgList[self.index]


iv = ImageViewer()

root = Tk()
app = Window(root)
app.set_imageViewer(iv)
app.fwd()
root.wm_title("Tkinter window")
root.geometry("1280x1000")
root.mainloop()
