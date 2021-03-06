
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

    model = Model(rootDir, 3)
    
    app = App()
    view = View(model)
    view.Title = 'LOLview'

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
