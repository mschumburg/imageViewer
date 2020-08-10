import wx
from controller import Controller


if __name__ == '__main__':
    app = wx.App(False)
    c = Controller(app)
    app.MainLoop()

