import wx
from timer import Timer

class ViewWx(wx.Frame):
    # PhotoMaxSize = 1280
    t = Timer()

    def __init__(self, model):
        wx.Frame.__init__(self, None)
        self.model = model

        self.SetSize(1280, 720)
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Bind(wx.EVT_CHAR_HOOK, self.keyPress)

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(wx.Colour(100, 0, 0))


        #self.imgPanel = wx.Panel(self.mainPanel)
        #self.imgPanel.SetBackgroundColour(wx.Colour(0, 150, 0))
        #self.imgPanel.SetSize((500, 500))
        #self.imgPanel.SetMaxSize((500, 500))
        #self.imgPanel.SetMinSize((500, 500))
        self.mainPanel.SetSize(1280, 720)
        
        mainBox = wx.BoxSizer(wx.VERTICAL)
        mainBox.Add(self.mainPanel, 0, wx.EXPAND, 0)
        mainBox.SetSizeHints(self)
        self.SetSizer(mainBox)

        self.mainPanel.SetSize(1280, 720)

        # self.imgPanel = wx.Panel(self.mainPanel)
        # self.imgPanel.SetBackgroundColour(wx.Colour(0, 150, 0))
        # self.imgPanel.SetSize((500, 500))
        # self.imgPanel.SetMaxSize((500, 500))
        # self.imgPanel.SetMinSize((500, 500))


        

        # self.mainPanel.SetSize(1280, 720)
        # s = self.mainPanel.GetSize()
        # print(s)
        # self.model.setSize(s[0], s[1])
        # img = self.model.getNextImg()
        # self.imageCtrl = wx.StaticBitmap(self.mainPanel, wx.ID_ANY, img)

        # sizer_v = wx.BoxSizer(wx.VERTICAL)
        # sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        # sizer_h.Add(self.imageCtrl, 1, wx.CENTER)
        # sizer_v.Add(sizer_h, 1, wx.CENTER)
        # self.mainPanel.SetSizer(sizer_v)







        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.imgPanel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        # self.sizer.SetSizeHints(self.imgPanel)
        # self.mainPanel.SetSizer(self.sizer)

        # self.SetSize(1280, 720)

        # s = self.mainPanel.GetSize()
        # self.model.setSize(s[0], s[1])

        # img = self.model.getNextImg()
        # self.imageCtrl = wx.StaticBitmap(self.mainPanel, wx.ID_ANY, img)

        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # #sizer.Add(self.imageCtrl, 1, wx.EXPAND | wx.ALL, 100)
        # self.sizer.Add(self.imageCtrl, 1, wx.EXPAND, 0)
        # self.sizer.SetSizeHints(self.mainPanel)
        # self.mainPanel.SetSizer(self.sizer)


        # OLD #############################


        # self.SetSize(1280, 720)

        # self.panel = wx.Panel(self)
        # self.panel.SetSize(1100, 600)
        # self.model.setSize(1100, 600)

        # self.SetBackgroundColour(wx.Colour(30, 30, 30))

        # img = self.model.getNextImg()

        # self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, img)

        #self.resized = False # the dirty flag
        #self.Bind(wx.EVT_SIZE,self.OnSize)
        #self.Bind(wx.EVT_IDLE,self.OnIdle)

        #self.panel.Bind(wx.EVT_CHAR_HOOK, self.keyPress)
        #self.mainPanel.Refresh()
        self.Show()
    
    def OnSize(self,event):
        self.resized = True # set dirty

    def OnIdle(self,event):
        if self.resized: 
            # take action if the dirty flag is set
            print("New size:", self.GetSize())
            newSize = self.GetSize()
            self.resized = False # reset the flag
            self.model.setSize(newSize[0] - 15, newSize[1] - 40)
            self.mainPanel.SetSize(newSize[0] - 15, newSize[1] - 40)

            img = self.model.getCurrentImg()
            self.imageCtrl.SetBitmap(img)

            self.mainPanel.Refresh()
    
    def keyPress(self, event):
        keycode = event.GetKeyCode()
        panelSize = self.mainPanel.GetSize()

        if keycode == wx.WXK_RIGHT:
            img = self.model.getNextImg()
            self.imageCtrl.SetBitmap(img)
            self.Update()
            self.Refresh()
            
            #self.sizer.Add(self.imageCtrl, 1, wx.EXPAND, 0)
            #self.sizer.SetSizeHints(self.mainPanel)
            #self.mainPanel.SetSizer(self.sizer)
            #self.mainPanel.Refresh()
            #self.mainPanel.Refresh()
            #self.mainPanel.Update()


        if keycode == wx.WXK_LEFT:
            img = self.model.getPrevImg()
            self.imageCtrl.SetBitmap(img)
            self.mainPanel.Refresh()

        event.Skip()
