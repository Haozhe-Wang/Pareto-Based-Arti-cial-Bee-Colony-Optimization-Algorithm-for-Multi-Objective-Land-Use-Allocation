#!/usr/bin/env python
import math
try:
    import numpy as np
except:
    raise ImportError("Numpy module not installed.")

from implementation import ABCalgorithm,exhibit



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
                        value_constrain[name]=[float(low),float(high)]
                    except Exception as e:

                        msg = "Error Found When Reading Data Constrains: %s\n"%e
                        with open("error.log","a") as f2:
                            f2.write(msg)
                        raise ReadConstrainError(msg)
    return value_constrain,landType_thr


def constraintCheck(matrix):
    #todo add constrain check
    pass


def run():

    # creates model
    ndim = int(2)
    value_constrain,landType_thr= readConstrain()
    print(landType_thr)

    model = ABCalgorithm.BeeHive(
                         10,  10,
                         value_constrain=value_constrain,
                         landType_thr=landType_thr,
                         numb_bees =  1000       ,
                         max_itrs  =  50       ,
                         verbose=True)
    archive = model.run()
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

