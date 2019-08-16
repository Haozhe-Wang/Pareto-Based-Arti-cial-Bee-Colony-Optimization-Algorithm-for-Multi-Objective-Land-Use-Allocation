# import numpy as np
from implementation.readTIFgraph import Reader
from implementation.generateWeight import WeightsCreater
import sys
# sys.setrecursionlimit(100000)


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
    TEMPLATE = {'top':[-1,0],'right':[0,1],'bottom':[1,0],'left':[-1,0],
                'top-right':[-1,1],'bottom-right':[1,1],'bottom-left':[1,-1],'top-left':[-1,-1]}
    # this will generate data from all objectives passed in fileMaps
    #this generator is based on the real data set
    # will guess data based on nearest value from the current raster cell
    # the decision of nearest value is based both on weight and on distance
    def __init__(self,fileMaps,typeMaps,weights,row=None,col=None,numLandType=None):
        """
        :param fileMaps:  dict key: is the objective name,value is the file name where it is located. Note: Must include a key called landType
        :param typeMaps:  dict key: is the number in landUseType.tif file, value is the land type name
        :param weights:   list this is list of lists, each cell contains a dictionary
        :param row: int   the maximum number of rows to be generated
        :param col: int   the maximum number of columns to be generated
        :param numObj:    the number of objectives involved.
        """
        self._readerMaps={}
        self._fileMaps = fileMaps # i,e. 氮净化:realData\part(1)\DanJingHua1.tif
        assert "landType" in self._fileMaps
        self._row = row
        self._col = col
        self._weights= weights
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
                for objective,reader in self._readerMaps.items():
                    if objective == "landType":
                        continue
                    value=reader.getFile()[numR][numC]
                    data_list = [0] * self._numLandType
                    data_list[index] = value
                    data_dict[objective]=data_list
                    result_row.append(data_dict)
            self._result.append(result_row)
    def completeGraph(self):
        for row in range(self._row):
            for col in range(self._col):
                data_dict = self._result[row][col]
                for name,datas in data_dict.items():
                    for index,data in enumerate(datas):
                        if type(data)==int:
                            self.search(row,col,name,index)
                print(self._result[row][col])
    '''
    # def search(self,row,col,name,index,curr_min_distance=0,found_distance=sys.float_info.max):
    #     weight = self._weights[row][col]
    #     weight = sorted(weight.items(), key=lambda arg: arg[1] if arg[1] != None else sys.float_info.max)
    #     # curr_min_distance+=weight[0][1]
    #     found_value=0
    #     # if curr_min_distance>=found_distance:
    #     #     return (found_distance,0)
    #     waiting_list=[]
    #     for pos in weight:
    #         if pos[1] != None:
    #             direction = generator1.TEMPLATE[pos[0]]
    #             newX = row + direction[0]
    #             newY = col + direction[1]
    #             distance = curr_min_distance+pos[1]
    #             if distance<found_distance:
    #                 value = self._result[newX][newY][name][index]
    #                 if type(value)!=int:
    #                     found_distance=distance
    #                     found_value=value
    #                     break
    #                 else:
    #                     waiting_list.append((newX,newY))
    #     if waiting_list==[] or curr_min_distance+weight[0][1]>=found_distance:
    #         return (found_distance, found_value)
    #     new_result=[]
    #     for new_cell in waiting_list:
    #         new_result.append(self.search(new_cell[0],new_cell[1],name,index,curr_min_distance+weight[0][1],found_distance))
    #     new_result=sorted(new_result)
    #     if len(new_result)>0 and new_result[0][0]<found_distance:
    #         return (new_result[0],new_result[1])
    #     return (found_distance,0)
    '''
    def search(self,row,col,name,index):
        # stack=[(row,col)]
        queue = PriorityQueue()
        queue.add(priorityItem((row,col),0))
        foot_print={(row,col)}
        # min_distance_stack=[0]
        found_distance = sys.float_info.max
        found_value=0
        # while len(stack)>0:
        while queue.length()>0:
            # next_pos=stack.pop()
            next_item = queue.remove()
            next_pos = next_item.item
            r = next_pos[0]
            c = next_pos[1]
            curr_min_distance = next_item.priority
            weight = self._weights[r][c]
            weight=sorted(weight.items(), key=lambda arg: arg[1] if arg[1] != None else sys.float_info.max)
            for pos in weight:
                if pos[1] != None:
                    direction = generator1.TEMPLATE[pos[0]]
                    newX = r+direction[0]
                    newY = c+direction[1]
                    if newX>=0 and newX<self._row and newY>=0 and newY<self._col:
                        distance = curr_min_distance + pos[1]
                        if distance < found_distance:
                            value = self._result[newX][newY][name][index]
                            if type(value)!=int:
                                found_distance=distance
                                found_value = value
                                break
                            else:
                                if (newX,newY) not in foot_print:
                                    # stack.append((newX,newY))
                                    queue.add(priorityItem((newX,newY),distance))
                                    foot_print.add((newX,newY))
                        else:
                            break
            # min_distance_stack.append(curr_min_distance+weight[0][1])
        # for pos in foot_print:
        #     self._result[pos[0]][pos[1]][name][index]=found_value
        self._result[row][col][name][index] = found_value
        # for i in sorted(foot_print):
        #     print(i)



    def getResult(self):
        return self._result
    result = property(getResult)


    @staticmethod
    def getIndexFromLandType(num):
        # if change land type number, please change here!!!!
        return num-11
class priorityItem():
    def __init__(self,item,priority):
        self._item=item
        self._priority = priority
    def getPriority(self):
        return self._priority
    def getItem(self):
        return self._item
    def __str__(self):
        return "%s\t%s"%(self.item,self.priority)
    def __gt__(self, other):
        return self._priority>other.priority
    def __lt__(self, other):
        return self._priority<other.priority
    def __eq__(self, other):
        return self._priority==other.priority
    def __le__(self, other):
        return self._priority <= other.priority
    def __ge__(self, other):
        return self._priority >= other.priority
    item=property(getItem)
    priority = property(getPriority)
class PriorityQueue():
    def __init__(self):
        self._queue = []
        self._length = 0
    def add(self,item):
        assert isinstance(item,priorityItem)
        i = self._length
        self._queue.append(item)
        parent= (i-1)//2
        while parent>=0 and self._queue[parent]>self._queue[i]:
            self._queue[parent],self._queue[i]=self._queue[i],self._queue[parent]
            i=parent
            parent=(i-1)//2
        self._length+=1
    def remove(self):
        if self._length<=0:
            return
        if self._length==1:
            self._length-=1
            return self._queue[0]
        self._length-=1
        self._queue[0],self._queue[-1]=self._queue[-1],self._queue[0]
        item = self._queue.pop()
        i=0
        leftchild = 2*i+1
        rightchild = 2*i+2
        while leftchild<self._length and self._queue[i]>self._queue[leftchild]:
            if rightchild<self._length and self._queue[i]>self._queue[rightchild]:
                self._queue[i], self._queue[rightchild] = self._queue[rightchild], self._queue[i]
                i=rightchild
            else:
                self._queue[i], self._queue[leftchild] = self._queue[leftchild], self._queue[i]
                i=leftchild
            leftchild = 2 * i + 1
            rightchild = 2 * i + 2
        return item
    def length(self):
        return self._length



class Queue():
    def __init__(self):
        self._head = 0
        self._tail = 0
        self._length=0
        self._queue=[0]*1

    def add(self,item):
        self._queue[self._tail]=item
        self._length+=1
        if self._tail == len(self._queue)-1:
            self._tail=0
        else:
            self._tail+=1
        if self._tail == self._head:
            self._resize()
    def _resize(self):
        temp_list=[0]*self._length*2
        for i in range(self._length):
            temp_list[i]=self._remove()
        self._head=0
        self._tail=self._length
        self._queue=temp_list
    def remove(self):
        item = self._remove()
        if item!=None:
            self._length -= 1
        return item

    def _remove(self):
        if self._length==0:
            return None
        item = self._queue[self._head]
        if self._head == len(self._queue)-1:
            self._head=0
        else:
            self._head+=1
        return item
    def __str__(self):
        result=""
        head= self._head
        for i in range(self._length):
            result+="%s "%self._remove()
        self._head=head
        return  result


if __name__ == "__main__":
    fileMaps= {"landType":'realData\part(1)\LandUseType11.tif',
               "氮净化":"realData\part(1)\DanJingHua1.tif",
               "水源涵养":'realData\part(1)\ShuiYuanHanYang1.tif'}
    typeMaps = {11:"森林",12:'草地',13:'农田',14:'聚落',15:'湿地',16:'荒漠'}
    # g.readData()
    # result = g.getResult()
    # nums=[0]*6
    # for row in result:
    #     for val in row:
    #         temp = val["水源涵养"]
    #         for i,k in enumerate(temp):
    #             if type(k)!=int:
    #               nums[i]+=1
    # print(nums)
    '''
    q=PriorityQueue()
    a1=priorityItem(1,4)
    a2=priorityItem(2,3)
    a3=priorityItem(3,3)
    a4=priorityItem(6,6)
    q.add(a1)
    q.add(a2)
    q.add(a3)
    q.add(a4)
    for i in range(4):
        print(q.remove())

    '''
    a = WeightsCreater(row=144, col=144)
    a.create()
    g = generator1(fileMaps, typeMaps,a.getWeights(), 144, 144)
    g.readData()
    temp_result = g.result
    with open("orinaldata/originalData3.txt","w",encoding="UTF-8") as f:

        for c in temp_result:
            for b in c:
                f.write("%s"%b["氮净化"][2]+"\t")
            f.write("\n")

    g.completeGraph()

    # results = g.getResult()

    # with open("data2.txt","w",encoding="UTF-8") as f:
    #     for row in results:
    #         for col in row:
    #             col_v=""
    #             for i in range(6):
    #                 v = ""
    #                 for name,values in col.items():
    #                     v+="%s,"%values[i]
    #                 v=v[0:-1]
    #                 col_v+=v+" "
    #             f.write(col_v+"\n")


