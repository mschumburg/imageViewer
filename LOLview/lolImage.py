class LolImage():
    def __init__(self, name, ext):
        x = ext.lower()
        self.name = name
        self.ext = [x]
        self.is_jpg = False
        self.data = None
        self.isProcessed = False

        self.is_liked = False

        self.focalLength = ''
        self.iso = ''
        self.aperture = ''
        self.exposureTime = ''

        if x == '.jpg' or x == '.jpeg':
            self.is_jpg = True
    
    def addExt(self, ext):
        x = ext.lower()

        self.ext.append(x)
        
        if x == '.jpg' or x == '.jpeg':
            self.is_jpg = True
    
    def getFileName(self):
        if self.is_jpg:
            return self.name + '.jpg'
        else:
            return self.name + '.RAF'
    
    def getString(self):
        return self.name + ' ' + str(self.ext) + ' ' + str(int(self.focalLength)) + 'mm f' + str(self.aperture)

    def __str__(self):
        return self.name + ' ' + str(self.ext) + ' ' + str(self.focalLength) + ' ' + str(self.aperture)