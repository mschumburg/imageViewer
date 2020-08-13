import glob
import time
import os

import wx
import exifread

from pathlib import Path

from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

import rawpy

from timer import Timer


class LolImage():
    def __init__(self, name, ext):
        x = ext.lower()
        self.name = name
        self.ext = [x]
        self.is_jpg = False
        self.data = None
        self.isProcessed = False

        if x == '.jpg' or x == '.jpeg':
            self.is_jpg = True
    
    def addExt(self, ext):
        x = ext.lower()

        self.ext.append(x)
        
        if x == '.jpg' or x == '.jpeg':
            self.is_jpg = True
    
    def getPath(self):
        if self.is_jpg:
            return self.name + '.jpg'
        else:
            return self.name + '.RAF'
        

    def __str__(self):
        return self.name + ' : ' + str(self.ext)


class Model():
    imgList = []
    index = -1
    rootDir = 'X:/Photography/2019/2019.10_Soller/'
    rootDir = './imgRaw/'
    rootDir = './img/2/'
    PhotoMaxSize = 1280
    panelW = 0
    panelH = 0

    preRenderCount = 0

    t = Timer()

    def __init__(self):
        imgList = []

        for file in sorted(glob.glob(self.rootDir + '*')):
            if os.path.isdir(file):
                continue

            p = Path(file)
            ext = p.suffix
            stem = p.stem

            if len(imgList) > 0 and stem == imgList[len(imgList) - 1].name:
                imgList[len(imgList) - 1].addExt(ext)
            else:
                imgList.append(LolImage(stem, ext))
        
        self.imgList = imgList

        #self.preRender(3)


    def preRender(self):
        # if self.index == -1 || self.index == 0:
        #     for i in range(batchSize):
        #         pass
        if self.preRenderCount == 0:
            return
       
        index = self.index

        if index < 0:
            index = 0

        # nach vorne rendern
        for i in range(index, index + self.preRenderCount):
            print('Prerender at Index: ' + str(i))
            img = self.getAtIndexImg(i)
            self.imgList[i].isProcessed = True
            self.imgList[i].data = img

    def renderNext(self):
        self.t.start()
        renderIndex = self.index + self.preRenderCount
        
        if renderIndex < len(self.imgList) :
            img = self.getAtIndexImg(renderIndex)
            self.imgList[renderIndex].isProcessed = True
            self.imgList[renderIndex].data = img
            print('Rendered at Index: ' + str(renderIndex))

        if self.index >= self.preRenderCount:
            print('Delete index: ' + str(self.index - self.preRenderCount))
            self.imgList[self.index - self.preRenderCount].data = None
        self.t.stop()

    def getSize(self, w, h):
        if w > h:
            newW = self.PhotoMaxSize
            newH = self.PhotoMaxSize * h / w
        else:
            newH = self.PhotoMaxSize
            newW = self.PhotoMaxSize * w / h
        
        return [newW, newH]

    def getSize2(self, w, h):
        ratio = min(self.panelW / w, self.panelH / h)
        newW = int(w * ratio)
        newH = int(h * ratio)

        return [newW, newH]

    def getAtIndexImg(self, index):
        imgPath = self.rootDir + self.imgList[index].getPath()

        if self.imgList[index].is_jpg:
            f = open(imgPath, 'rb')
            exifData = exifread.process_file(f, details=False)
            f.close()

            img = wx.Image(imgPath, wx.BITMAP_TYPE_ANY)
            
            if 'Image Orientation' in exifData.keys():
                orientation = exifData['Image Orientation']
                val = orientation.values
                if 8 in val:
                    img = img.Rotate90(clockwise=False)
            
            newSize = self.getSize2(img.GetWidth(), img.GetHeight())
            img = img.Scale(newSize[0], newSize[1])

            return img.ConvertToBitmap()
        else:
            rgb = None
            with rawpy.imread(imgPath) as raw:
                rgb = raw.postprocess(no_auto_bright=True, half_size=True)

            pimg = Image.fromarray(rgb)

            wxImg = wx.Image(*pimg.size)

            rgbString = pimg.convert('RGB').tobytes()
            wxImg.SetData(rgbString)

            newSize = self.getSize2(wxImg.GetWidth(), wxImg.GetHeight())
            wxImg = wxImg.Scale(newSize[0], newSize[1])

            wxBmap = wxImg.ConvertToBitmap()

            return wxBmap
    
    def getNextImg(self):
        self.index += 1

        if self.index > (len(self.imgList) - 1):
            return None

        if self.imgList[self.index].isProcessed:
            return self.imgList[self.index].data

        return self.getAtIndexImg(self.index)
    
    def getNextImgByPath(self):
        self.index += 1

        return self.rootDir + self.imgList[self.index].getPath()
    
    def getPrevImg(self):
        self.index -= 1

        return self.getAtIndexImg(self.index)
    
    def getCurrentImg(self):
        return self.getAtIndexImg(self.index)

    def setSize(self, w, h):
        self.panelW = w
        self.panelH = h