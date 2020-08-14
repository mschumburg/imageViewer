import wx
import exifread
from timer import Timer
import rawpy
from PIL import Image, ImageTk


panelW =  1920
panelH = 1080

def renderJpg():
    imgPath = './img/DSCF4845.JPG'

    f = open(imgPath, 'rb')
    exifData = exifread.process_file(f, details=False)
    f.close()

    img = wx.Image(imgPath, wx.BITMAP_TYPE_ANY)

    if 'Image Orientation' in exifData.keys():
        orientation = exifData['Image Orientation']
        val = orientation.values
        if 8 in val:
            img = img.Rotate90(clockwise=False)

    newSize = getSize2(img.GetWidth(), img.GetHeight())
    img = img.Scale(newSize[0], newSize[1])

    imgData = img.ConvertToBitmap()

def renderRaw():
    imgPath = './img/DSCF8803.RAF'
    rgb = None
    with rawpy.imread(imgPath) as raw:
        rgb = raw.postprocess(no_auto_bright=True, half_size=True)

    pimg = Image.fromarray(rgb)

    wxImg = wx.Image(*pimg.size)

    rgbString = pimg.convert('RGB').tobytes()
    wxImg.SetData(rgbString)

    newSize = getSize2(wxImg.GetWidth(), wxImg.GetHeight())
    wxImg = wxImg.Scale(newSize[0], newSize[1])

    imgData = wxImg.ConvertToBitmap()

def getSize2(w, h):
    ratio = min(panelW / w, panelH / h)
    newW = int(w * ratio)
    newH = int(h * ratio)

    return [newW, newH]

if __name__ == '__main__':
    app = wx.App(False)
    t = Timer()
    t.start()
    #renderJpg()
    renderRaw()
    t.stop()




