#!/usr/bin/env python
import math
from readTIFgraph import Reader
try:
    import numpy as np
except:
    raise ImportError("Numpy module not installed.")

import ABCalgorithm,exhibit



class ReadConstrainError(Exception):
    pass


def evaluator(vector):
    # vector = np.array(vector)
    #
    # return (a - vector[0]) ** 2 + b * (vector[1] - vector[0] ** 2) ** 2
    return vector
   #todo: add evaluate function --> Different objective with different function to calculate the value \
   #todo: of the raster cell of the objective


def readConstrain():
    value_constrain ={}
    read_type = 0
    landType_thr={}
    with open('dataConstrain.txt','r',encoding="UTF-8") as f:
        for constrain in f:
            constrain = constrain.strip()
            if constrain == "value constrain":
                read_type=1
            elif constrain == "land type constrain":
                read_type=2
            else:
                name, low, high = constrain.split()
                if read_type==2:

                    try:
                        landType_thr[name]=[int(low),int(high)]
                        assert landType_thr[name][0]<=landType_thr[name][1]
                    except Exception as e:
                        msg = "Error Found When Reading Land Type Constrains"
                        with open("error.log","a") as f2:
                            f2.write(msg)
                        raise ReadConstrainError(msg)
                elif read_type ==1:
                    try:
                        landType,constrainName = name.split("-")
                        if landType in value_constrain:
                            temp = value_constrain[landType]
                        else:
                            temp={}
                        temp[constrainName]=[float(low),float(high)]
                        value_constrain[landType]=temp
                    except Exception as e:

                        msg = "Error Found When Reading Data Constrains: %s\n"%e
                        with open("error.log","a") as f2:
                            f2.write(msg)
                        raise ReadConstrainError(msg)
    return value_constrain,landType_thr


def constraintCheck(matrix):
    #todo add constrain check
    pass
def readUnchangeArea(path,values):

    reader = Reader(path)
    graph = reader.getFile()
    result = {}
    typeMaps = {11: "森林", 12: '草地', 13: '农田', 14: '聚落', 15: '湿地', 16: '荒漠'}
    for r,row in enumerate(graph):
        for c,col in enumerate(row):
            if col in values:
                result[(r,c)]=typeMaps[col]
    return result


def run():

    # creates model
    ndim = int(2)
    value_constrain,landType_thr= readConstrain()
    print(landType_thr)
    # occupied={(1,2):"湿地",(5,3):"森林",(0,0):"聚落"}
    occupied = readUnchangeArea('realData\part(1)\LandUseType11.tif',[14])
    model = ABCalgorithm.BeeHive(
                         140,  140,2,
                         occupied = occupied    ,
                         landType_thr=landType_thr,
                         numb_bees =  40       ,
                         max_itrs  =  30       ,
                         verbose=True)
    archive = model.run()
    model.writeToFile("solutions.txt")
    dataSet=[]
    for bee in archive:
        if len(dataSet)==0:
            for v in bee.vector:
                dataSet.append([v])
        else:
            for i,v in enumerate(bee.vector):
                dataSet[i].append(v)
    exhibit.show(dataSet)



if __name__ == "__main__":
    run()

