import wx
from timer import Timer

class View(wx.Frame):
    t = Timer()

    def __init__(self, model):
        wx.Frame.__init__(self, None)
        self.model = model

        self.panel = wx.Panel(self)

        self.panel.SetBackgroundColour('#1c1c1c')
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.midPan = wx.Panel(self.panel)
        self.midPan.SetBackgroundColour('#1c1c1c')

        self.vbox.Add(self.midPan, wx.ID_ANY, wx.EXPAND | wx.ALL, 45)
        self.panel.SetSizer(self.vbox)

        img = wx.Bitmap(10, 10)
        self.imageCtrl = wx.StaticBitmap(self.midPan, wx.ID_ANY, img)

        self.Bind(wx.EVT_CHAR_HOOK, self.keyPress)

        self.Maximize(True)
        self.Show()

        midPanSize = self.midPan.GetSize()

        self.model.setSize(midPanSize[0], midPanSize[1])
        self.model.preRender()
        self.setNextImage()
        
    def OnSize(self,event):
        self.resized = True # set dirty

    def OnIdle(self,event):
        if self.resized: 
            # take action if the dirty flag is set
            print("New size:", self.GetSize())
            # newSize = self.GetSize()
            # self.resized = False # reset the flag
            # self.model.setSize(newSize[0] - 15, newSize[1] - 40)
            # self.mainPanel.SetSize(newSize[0] - 15, newSize[1] - 40)

            # img = self.model.getCurrentImg()
            # self.imageCtrl.SetBitmap(img)

            # self.mainPanel.Refresh()
            midPanSize= self.midPan.GetSize()
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
            img = self.renderImage(img)

            #threading.Thread(target=self.model.renderNext).start()
        
    def setPrevImage(self):
        img = self.model.getPrevImg()

        if img is None:
            return
        else: 
            img = self.renderImage(img)

            #threading.Thread(target=self.model.renderPrev).start()

    def keyPress(self, event):
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_RIGHT:
            self.setNextImage()


        if keycode == wx.WXK_LEFT:
            self.setPrevImage()
            
        event.Skip()
