import wx
from lolImage import LolImage
from timer import Timer
import webbrowser

class View(wx.Frame):
    t = Timer()

    is_fullscreen = False
    is_whiteBg = False

    def __init__(self, model):
        wx.Frame.__init__(self, None)
        self.model = model

        self.panel = wx.Panel(self)

        self.panel.SetBackgroundColour('#1c1c1c')
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.midPan = wx.Panel(self.panel)
        #self.midPan.SetBackgroundColour('#1c1c1c')

        self.vbox.Add(self.midPan, wx.ID_ANY, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 60)
        self.panel.SetSizer(self.vbox)

        img = wx.Bitmap(10, 10)
        #img = wx.Image('./assets/img/main.png', wx.BITMAP_TYPE_ANY)
        self.imageCtrl = wx.StaticBitmap(self.midPan, wx.ID_ANY, img)
        #self.imageCtrl = wx.StaticBitmap(self.midPan, wx.ID_ANY, img.ConvertToBitmap())

        self.toolPanel = wx.Panel(self.panel, size=(600, 30))
        self.textField = wx.StaticText(self.toolPanel, wx.ID_ANY, label='')
        self.textField.SetForegroundColour((120, 120, 120))
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_THIN)
        self.textField.SetFont(font)
        #toolPanel.SetBackgroundColour('#ffff00')
        self.vbox.Add(self.toolPanel, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.TOP, 15)

        self.Bind(wx.EVT_CHAR_HOOK, self.keyPress)

        self.Maximize(True)
        self.Show()

        img = wx.Image('../assets/img/main.png', wx.BITMAP_TYPE_ANY)
        self.renderImage(img.ConvertToBitmap())

        midPanSize = self.midPan.GetSize()
        self.model.setSize(midPanSize[0], midPanSize[1])
        
        #self.model.preRender()
        #self.setNextImage()
        
    def OnSize(self,event):
        self.resized = True # set dirty

    def OnIdle(self,event):
        if self.resized: 
            print("New size:", self.GetSize())
            midPanSize = self.midPan.GetSize()
            self.model.setSize(midPanSize[0], midPanSize[1])
    
    def renderImage(self, img):
        midPanSize= self.midPan.GetSize()

        imgSize = img.GetSize()

        xDelta = 0
        yDelta = 0

        if midPanSize[0] > imgSize[0]:
            xDelta = int((midPanSize[0] - imgSize[0]) / 2)
        
        if midPanSize[1] > imgSize[1]:
            yDelta = int((midPanSize[1] - imgSize[1]) / 2)
        
        self.imageCtrl.SetBitmap(img)
        self.imageCtrl.SetPosition((xDelta, yDelta))

    def setNextImage(self):
        img = self.model.getNextImg()

        if img is None:
            return
        else: 
            self.renderImage(img.data)
            self.textField.SetLabel(img.getString())
        
    def setPrevImage(self):
        img = self.model.getPrevImg()

        if img is None:
            return
        else: 
            self.renderImage(img.data)
            self.textField.SetLabel(img.getString())

    def keyPress(self, event):
        keycode = event.GetKeyCode()
        # print(keycode)

        if keycode in [wx.WXK_RIGHT, 68]:
            self.setNextImage()


        if keycode in [wx.WXK_LEFT, 65]:
            self.setPrevImage()
        
        if keycode == wx.WXK_SPACE:
            self.is_fullscreen = not self.is_fullscreen

            if self.is_fullscreen:
                self.ShowFullScreen(True)
            else:
                self.ShowFullScreen(False)
        
        if keycode == wx.WXK_ESCAPE:
            self.is_fullscreen = False
            self.ShowFullScreen(False)
        
        # b
        if keycode == 66:
            self.is_whiteBg = not self.is_whiteBg

            if self.is_whiteBg:
                self.panel.SetBackgroundColour('#f7f7f7')
                self.panel.Refresh()
            else:
                self.panel.SetBackgroundColour('#1c1c1c')
                self.panel.Refresh()

        # w
        if keycode == 87:
            self.model.like()

        # s
        if keycode in [wx.WXK_DOWN, 83]:
            dlg = wx.DirDialog(self, message='choose a folder')

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                
                self.model.setPath(path)
                self.model.preRender()
                self.setNextImage()
            
            dlg.Destroy()
        
        if keycode == 69:
            webbrowser.open('file:///' + self.model.getDir())
        
        if keycode == 84:
            pass
                    
        event.Skip()
