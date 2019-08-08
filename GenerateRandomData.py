import numpy as np
random = np.random.RandomState(0)
types =["湿地","森林","群落"]
with open("data.txt",'w',encoding="UTF-8") as f:
    for type in types:
        f.write("%s\n"%type)
        for i in range(10):
            row=""
            for k in range(10):

                row+="%f,%f "%(random.uniform(1, 10),random.uniform(5, 20))
            f.write(row)
            f.write("\n")

def printMatrix(matrix):
    for r in matrix:
        for k in r:
            print(k,end=" ")
        print('\n')