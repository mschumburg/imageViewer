import glob
import time
import os
import threading

import wx
import exifread

from pathlib import Path

from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
from exif import Image as ExifImage

import rawpy

from timer import Timer
from lolImage import LolImage

class Model():
    imgList = []
    index = -1
    # rootDir = 'X:/Photography/2019/2019.10_Soller/'
    # rootDir = './imgRaw/'
    # rootDir = './img/2/'
    # PhotoMaxSize = 1280
    panelW = 0
    panelH = 0

    preRenderCount = 0

    t = Timer()

    def __init__(self, rootDir, preRenderCount):
        self.rootDir = rootDir
        self.preRenderCount = preRenderCount

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
            self.renderImage(i)

    def renderNext(self):
        self.t.start()
        renderIndex = self.index + self.preRenderCount
        deleteIndex = self.index - (self.preRenderCount + 1)
        
        if renderIndex < len(self.imgList) :
            self.renderImage(renderIndex)
            print('Rendered at Index: ' + str(renderIndex))

        if deleteIndex >= 0:
            print('Delete index: ' + str(deleteIndex))
            self.imgList[deleteIndex].data = None
        self.t.stop()

    def renderPrev(self):
        renderIndex = self.index - self.preRenderCount
        deleteIndex = self.index + (self.preRenderCount + 1)

        if renderIndex >= 0:
            self.renderImage(renderIndex)
            print('Rendered at Index: ' + str(renderIndex))
        
        if deleteIndex < len(self.imgList):
            print('Delete index: ' + str(deleteIndex))
            self.imgList[deleteIndex].data = None

        
        #if self.index 

    # def getSize(self, w, h):
    #     if w > h:
    #         newW = self.PhotoMaxSize
    #         newH = self.PhotoMaxSize * h / w
    #     else:
    #         newH = self.PhotoMaxSize
    #         newW = self.PhotoMaxSize * w / h
        
    #     return [newW, newH]

    def getSize2(self, w, h):
        ratio = min(self.panelW / w, self.panelH / h)
        newW = int(w * ratio)
        newH = int(h * ratio)

        return [newW, newH]

    def renderImage(self, index):
        imgPath = self.rootDir + self.imgList[index].getPath()

        with open(imgPath,  'rb') as file:
            exifData2 = ExifImage(file)
        
        try:
            self.imgList[index].focalLength = exifData2.focal_length
            self.imgList[index].aperture = exifData2.f_number
            self.imgList[index].exposureTime = exifData2.exposure_time
            self.imgList[index].iso = exifData2.photographic_sensitivity
        except:
            pass


        # print(dir(img))

        print('New Index: ' + str(self.index))

        imgData = None

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

            self.imgList[index].data = img.ConvertToBitmap()
            self.imgList[index].isProcessed = True

            imgData = img.ConvertToBitmap()
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

            imgData = wxImg.ConvertToBitmap()
        
        self.imgList[index].data = imgData
        self.imgList[index].isProcessed = True
    
    def getNextImg(self):
        if self.index == (len(self.imgList) - 1):
            return None
        
        self.index += 1

        threading.Thread(target=self.renderNext).start()

        return self.imgList[self.index]

        # if self.imgList[self.index].isProcessed:
        #     return self.imgList[self.index].data

        # return self.renderImage(self.index)
    
    def getPrevImg(self):
        if self.index == 0:
            return None
        
        self.index -= 1

        threading.Thread(target=self.renderPrev).start()

        return self.imgList[self.index]
        
        # if self.imgList[self.index].isProcessed:
        #     return self.imgList[self.index].data

        # return self.renderImage(self.index)
    
    def getNextImgByPath(self):
        self.index += 1

        return self.rootDir + self.imgList[self.index].getPath()
    
    def getCurrentImg(self):
        return self.renderImage(self.index)

    def setSize(self, w, h):
        self.panelW = w
        self.panelH = h