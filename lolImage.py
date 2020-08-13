class LolImage():
    def __init__(self, name, ext):
        x = ext.lower()
        self.name = name
        self.ext = [x]
        self.is_jpg = False
        self.data = None
        self.isProcessed = False

        if x in ['.jpg', '.jpeg']:
            self.is_jpg = True
    
    def addExt(self, ext):
        x = ext.lower()

        self.ext.append(x)

        if x in ['.jpg', '.jpeg']:
            self.is_jpg = True
    
    def getPath(self):
        if self.is_jpg:
            return self.name + '.jpg'
        else:
            return self.name + '.RAF'
        
    def __str__(self):
        return self.name + ' : ' + str(self.ext)