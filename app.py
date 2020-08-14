
import wx
from model import Model
from view import View

class App(wx.App):
    def __init__(self):
        wx.App.__init__(self, False)

def main():
    rootDir = 'X:/Photography/2019/2019.10_Soller'
    #rootDir = './imgRaw/'
    #rootDir = './img/2/'
    rootDir = './img/'

    model = Model(rootDir, 2)
    
    app = App()
    view = View(model)

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
