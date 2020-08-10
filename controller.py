#import tkinter as Tk
from model import Model
#from view import View
from viewWx import ViewWx

class Controller:
    def __init__(self, app):
        self.model = Model()
        self.view = ViewWx(self.model)

    # def init_wx(self):
    #     self.r = ViewWx(self.model)
    
    # def init_tk(self):
    #     self.root = Tk.Tk()
    #     self.view = View(self.root, self.model)

    # def run_tk(self):
    #     self.root.title('Viewer')
    #     self.root.geometry('1280x720')
    #     self.root.mainloop()
