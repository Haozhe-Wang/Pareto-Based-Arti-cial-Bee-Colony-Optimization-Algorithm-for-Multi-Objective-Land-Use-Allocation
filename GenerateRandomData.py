# import numpy as np
from implementation.readTIFgraph import Reader
# # the steps below are only used for extremely simple generation of data to data.txt. No worth for using
# random = np.random.RandomState(0)
# types =["湿地","森林","群落"]
# with open("data.txt",'w',encoding="UTF-8") as f:
#     for type in types:
#         f.write("%s\n"%type)
#         for i in range(10):
#             row=""
#             for k in range(10):
#
#                 row+="%f,%f "%(random.uniform(1, 10),random.uniform(5, 20))
#             f.write(row)
#             f.write("\n")

def printMatrix(matrix):
    output=""
    for r in matrix:
        for k in r:
            print(k,end=" ")
            output+=k+" "
        print('\n')
        output+='\n'
    return output
def getMatrix(matrix):
    output=""
    for r in matrix:
        for k in r:
            output+=k+" "
        output+='\n'
    return output

class generator1():
    # this will generate data from all objectives passed in fileMaps
    #this generator is based on the real data set
    # will guess data based on nearest value from the current raster cell
    # the decision of nearest value is based both on weight and on distance
    def __init__(self,fileMaps,typeMaps,row=None,col=None,numLandType=None):
        """
        :param fileMaps:  dict key: is the objective name,value is the file name where it is located. Note: Must include a key called landType
        :param typeMaps:  dict key: is the number in landUseType.tif file, value is the land type name
        :param row: int the maximum number of rows to be generated
        :param col: int the maximum number of columns to be generated
        :param numObj:    the number of objectives involved.
        """
        self._readerMaps={}
        self._fileMaps = fileMaps # i,e. 氮净化:realData\part(1)\DanJingHua1.tif
        assert "landType" in self._fileMaps
        self._row = row
        self._col = col
        self._typeMaps = typeMaps
        if numLandType == None:
            self._numLandType = len(self._typeMaps)
        else:
            self._numLandType = numLandType
        # the result is a list of lists, and the inner list contains row numbers of dictionaries
        # which key is objective,value is a list of values,
        # the list's index corresponds to each land type which is determined by getIndexFromLandType(num) function
        self._result=[]
    def readData(self):
        for name,path in self._fileMaps.items():
            self._readerMaps[name]=Reader(path)
        landType = self._readerMaps["landType"].getFile()
        if self._row == None:
            self._row= len(landType)
            if self._row>0 and self._col == None:
                self._col = len(landType[0])
        for numR in range(self._row):
            result_row = []
            for numC in range(self._col):
                landType_num = landType[numR][numC]
                landTypeName = self._typeMaps[landType_num]
                data_dict = {}
                index = generator1.getIndexFromLandType(landType_num)
                print(index)
                for objective,reader in self._readerMaps.items():
                    if objective == "landType":
                        continue
                    value=reader.getFile()[numR][numC]
                    data_list = [0] * self._numLandType
                    data_list[index] = value
                    data_dict[objective]=data_list
                    result_row.append(data_dict)
            self._result.append(result_row)

    def getResult(self):
        return self._result
    result = property(getResult)


    @staticmethod
    def getIndexFromLandType(num):
        # if change land type number, please change here!!!!
        return num-11

if __name__ == "__main__":
    fileMaps= {"landType":'realData\part(1)\LandUseType11.tif',
               "氮净化":"realData\part(1)\DanJingHua1.tif",
               "水源涵养":'realData\part(1)\ShuiYuanHanYang1.tif'}
    typeMaps = {11:"森林",12:'草地',13:'农田',14:'聚落',15:'湿地',16:'荒漠'}
    g= generator1(fileMaps,typeMaps,100,100)
    g.readData()
    result = g.getResult()
    for row in result:
        for val in row:
            print(val)


