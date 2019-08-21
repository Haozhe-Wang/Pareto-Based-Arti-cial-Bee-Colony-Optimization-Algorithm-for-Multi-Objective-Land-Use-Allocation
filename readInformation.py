def readInformation(types):

    infos={}
    with open("data2.txt","r",encoding="UTF-8") as f:
        datas = []
        cur_type = f.readline().strip()
        for line in f:
            line = line.strip()
            if line in types:
                infos[cur_type]=datas
                cur_type=line
                datas = []
                continue
            temp = line.split()
            data=[]
            for d in temp:
                d=d.split(",")
                data.append(list(map(float,d)))
            datas.append(data)
        infos[cur_type] = datas
    return infos
if __name__ == "__main__":
    from GenerateRandomData import printMatrix
    infos=readInformation(["湿地","森林","群落"])
    for key,matrix in infos.items():
        print(key)

        printMatrix(matrix)
