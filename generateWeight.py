import math
class WeightsCreater():
    def __init__(self,matrix = None,row=100,col=100):
        self._matrix = matrix
        self._row = row
        self._col = col
        self._weights=[]


    def create(self):
        if self._matrix == None:
            self._matrix=self.generateWeightMatrix(self._row,self._col)
        self._row=len(self._matrix)
        if self._row>0:
            self._col = len(self._matrix[0])
        self.calculateWeights()
    def generateWeightMatrix(self,row,col):
        # this function is only used by testing
        # the result matrix should be replaced by real data
        return [[i for i in range(k,k+col)] for k in range(row)]
    def calculateWeights(self):

        for row in range(self._row):
            weight_row=[]
            for col in range(self._col):
                # weights data will stores the weight from all directions
                # the weights data goes from [top,right,bottom,left,top-right,bottom-right,bottom-left,top-left]
                template = ['top','right','bottom','left','top-right','bottom-right','bottom-left','top-left']
                weights_data={}
                for name in template:
                    weights_data[name] = None
                weight_row.append(weights_data)
            self._weights.append(weight_row)
        for row in range(self._row):
            for col in range(self._col):
                newX = row+1
                ifValidX = newX<self._row
                if ifValidX:
                    weight = self._matrix[newX][col]-self._matrix[row][col]
                    self._weights[row][col]["right"]=weight
                    self._weights[newX][col]["left"]=weight

                newY = col + 1
                if newY < self._col:
                    weight = self._matrix[row][newY] - self._matrix[row][col]
                    self._weights[row][col]["bottom"] = weight
                    self._weights[row][newY]["top"] = weight
                    if ifValidX:
                        weight = math.sqrt(self._weights[row][col]["bottom"]**2+self._weights[row][col]["right"]**2)
                        self._weights[row][col]["bottom-right"]=weight
                        self._weights[newX][newY]["top-left"]=weight
                newY=col-1
                if ifValidX and newY >=0:
                    weight = math.sqrt(self._weights[row][col]["top"]**2+self._weights[row][col]["right"]**2)
                    self._weights[row][col]["top-right"] = weight
                    self._weights[newX][newY]["bottom-left"] = weight
    def getWeights(self):
        return self._weights


if __name__ == "__main__":
    a= WeightsCreater(row=10,col=10)
    a.create()
    for k in a.getWeights():
        for z in k:
            print(z)



