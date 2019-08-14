import cv2
class Reader():
    def __init__(self,path,mode=-1):
        """

        :param paths: file paths to be read
        :param mode: the mode for reading tif files
        """
        self._path = path
        self._file = None
        self.read(mode)

    def read(self,mode):
        self._file=cv2.imread(self._path,mode)
    def changePath(self,path):
        self._path=path
    def getFile(self):
        return self._file
    def toList(self,toType=None):
        lst = []
        for row in self._file:
            if toType == None:
                lst=[val for val in row]
            else:
                lst=[toType(val) for val in row]
        return lst
if __name__ == "__main__":
    # file = cv2.imread("realData\part(1)\DanJingHua1.tif",2)
    file = cv2.imread("realData\part(1)\LandUseType11.tif",-2)
    # print(len(file))
    l=[0]*6
    for r in file:
        # print(len(r))
        for c in r:
            c=c-11
            l[c]+=1
    print(l)
