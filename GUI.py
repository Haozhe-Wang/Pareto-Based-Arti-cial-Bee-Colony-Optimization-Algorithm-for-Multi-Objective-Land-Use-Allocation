from tkinter import *
from tkinter import filedialog
from ABCalgorithm import *
import os
import readTIFgraph
import time
from threading import Thread
import exhibit
from multiprocessing import Process
class Interface():
    PARAM_KEY_TEMPLATE = ["row","col","dim","readFile","occupied","numb_bees","landType_thr",
                            "max_itrs","max_trials","max_PA","max_FS","mutate_per","verbose"]
    def __init__(self,root):
        self._root = root
        self._outputPath = os.getcwd()
        self._occupiedFile = os.getcwd()
        self._verbose= True
        self._executionProcess = None
        self._ifHaveOccupiedArea=False
        self._fileTypeMaps={"森林":11,'草地':12,'农田':13,'聚落':14,'湿地':15,'荒漠':16}
        self._fileTypeEntries=[]  # typo, this means the land type same as above
        self._args = [None, None, None,None, {}, 30, None, 100, 40, 100, 20, 0.3, True]
        self._entries = {}
        self.setWindow()
        self.createWedgets()
        # self._compusoryArea.nametowidget("row")["bg"]="green"
    def setWindow(self):
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        w = 800  # width for the Tk root
        h = 650  # height for the Tk root
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self._root.title('土地分配优化')
        self._root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self._root.resizable(width=True, height=True)
    def createWedgets(self):
        self.createCompusoryArea()
        self.createOptionalArea()
        self.createLandTypeInputArea()
        self.createOccupiedArea()
        self.createExecutionArea()
        self.createShowArea()

    def createCompusoryArea(self):
        self._compusoryArea = Frame(self._root)
        self._compusoryArea.pack()
        rowLabel = Label(self._compusoryArea, text="输入输出行数")
        rowEntry = Entry(self._compusoryArea, name="row")
        colLabel = Label(self._compusoryArea, text="输入输出列数")
        colEntry = Entry(self._compusoryArea, name="col")
        dimLabel = Label(self._compusoryArea, text="指标个数")
        dimEntry = Entry(self._compusoryArea, name="dim")

        v = StringVar(value=self._occupiedFile)
        def askFile():
            path = filedialog.askopenfilename(initialdir=v,
                                              title="选择文件",
                                              filetypes=(("txt 文件", "*.txt"),))
            v.set(path)
        readFileLabel = Label(self._compusoryArea,text="输入参考数据文件（仅支持.txt）")
        readFileEntry = Entry(self._compusoryArea, name="readFile", textvariable=v)
        occupiedSelectButton = Button(self._compusoryArea, text="选择文件",
                                    command=askFile)


        self._entries["row"]=rowEntry
        self._entries["col"] = colEntry
        self._entries["dim"] = dimEntry
        self._entries["readFile"] = readFileEntry
        rowLabel.grid(row=0, column=0)
        rowEntry.grid(row=0, column=1)

        colLabel.grid(row=1, column=0)
        colEntry.grid(row=1, column=1)

        dimLabel.grid(row=2, column=0)
        dimEntry.grid(row=2, column=1)

        readFileLabel.grid(row=3,column=0)
        readFileEntry.grid(row=3, column=1)
        occupiedSelectButton.grid(row=3, column=2)

    def createOptionalArea(self):
        boolVal = BooleanVar()
        boolVal.set(True)
        def changeVerbose():
            value = boolVal.get()
            if value == self._verbose:
                return
            else:
                self._verbose=value
            if self._verbose:
                self.createShowArea()
            else:
                self._showFrame.pack_forget()

        self._optionalArea = Frame(self._root)
        self._optionalArea.pack()

        numBeeLabel = Label(self._optionalArea,text = "多少只蜜蜂")
        numBeeEntry = Entry(self._optionalArea,name="numb_bees")
        numBeeEntry.insert(END,30)

        maxIterLabel = Label(self._optionalArea, text="循环次数（max iterations)")
        maxIterEntry = Entry(self._optionalArea, name="max_itrs")
        maxIterEntry.insert(END, 100)

        #函数中没有实现counter+=1
        # numBeeLabel = Label(self._optionalArea, text="多少次后放弃解")
        # numBeeEntry = Entry(self._optionalArea, name="max_trials")
        # numBeeEntry.insert(END, 40)

        maxPALabel = Label(self._optionalArea, text="pareto archive最大个数")
        maxPAEntry = Entry(self._optionalArea, name="max_PA")
        maxPAEntry.insert(END, 100)

        foodSourceLabel = Label(self._optionalArea, text="food source最大个数")
        foodSourceEntry = Entry(self._optionalArea, name="max_FS")
        foodSourceEntry.insert(END, 20)

        mutatePerLabel = Label(self._optionalArea, text="交换比率（mutate)")
        mutatePerEntry = Entry(self._optionalArea, name="mutate_per")
        mutatePerEntry.insert(END, 0.3)

        v = StringVar(value=self._outputPath)
        def askDir():
            self._outputPath = filedialog.askdirectory(initialdir=self._outputPath,
                                                       title="选择文件夹")
            v.set(self._outputPath)
        outputFileLabel = Label(self._optionalArea, text="输出到文件夹：")
        outputFileEntry = Entry(self._optionalArea, name="outputPath",textvariable = v)
        outputSelectButton = Button(self._optionalArea,text ="选择文件夹",
                                    command = askDir)



        self._entries["numb_bees"] = numBeeEntry
        self._entries["max_itrs"] = maxIterEntry
        self._entries["max_PA"] = maxPAEntry
        self._entries["max_FS"] = foodSourceEntry
        self._entries["mutate_per"] = mutatePerEntry
        self._entries["outputPath"] = outputFileEntry

        numBeeLabel.grid(row=0,column = 0)
        numBeeEntry.grid(row=0, column=1)

        maxIterLabel.grid(row=1, column=0)
        maxIterEntry.grid(row=1, column=1)

        maxPALabel.grid(row=2, column=0)
        maxPAEntry.grid(row=2, column=1)

        foodSourceLabel.grid(row=3, column=0)
        foodSourceEntry.grid(row=3, column=1)

        mutatePerLabel.grid(row=4, column=0)
        mutatePerEntry.grid(row=4, column=1)

        outputFileLabel.grid(row=5,column=0)
        outputFileEntry.grid(row=5,column=1)
        outputSelectButton.grid(row=5,column=2)

        verboseLabel = Label(self._optionalArea,text = "是否展示计算过程")
        verboseFrame = Frame(self._optionalArea)
        radioTrue = Radiobutton(verboseFrame, text='True', value =True, command=lambda: changeVerbose(),
                                indicatoron=0,variable = boolVal)
        radioFalse = Radiobutton(verboseFrame, text='False',value=False, command=lambda: changeVerbose(),
                                 indicatoron=0,variable = boolVal)
        radioTrue.pack(side=LEFT)
        radioFalse.pack(side=RIGHT)
        verboseLabel.grid(row=6,column=0)
        verboseFrame.grid(row=6,column=1)

    def createLandTypeInputArea(self):
        self._landTypeInputArea = Frame(self._root)
        self._landTypeInputArea.pack()
        self._landTypes = []

        def delete(event):
            self._landTypes.remove(event.master)
            event.master.destroy()


        def addANew():
            frameName = "landType%d"%len(self._landTypes)
            frame = Frame(self._landTypeInputArea,name=frameName)
            self._landTypes.append(frame)
            frame.pack(side = BOTTOM)
            names = ["类型",'下限','上限']
            i=0
            for name in names:
                typeLabel = Label(frame,text=name,name="typeLabel%d"%i)
                typeLabel.pack(side=LEFT)
                typeEntry = Entry(frame,name="typeEntry%d"%i)
                typeEntry.pack(side=LEFT)
                i+=1
            deleteButton = Button(frame,text = "删除",command = lambda :delete(deleteButton))
            deleteButton.pack(side=LEFT)




        remindFrame = Frame(self._landTypeInputArea)
        remindFrame.pack()
        remindLabel = Label(remindFrame,text = "添加土地类型范围")
        addButton = Button(remindFrame,text = "添加",command = addANew)
        remindLabel.pack(side=LEFT)
        addButton.pack(side=LEFT)

    def createOccupiedArea(self):
        self._occupiedFrame = Frame(self._root)
        self._occupiedFrame.pack()
        askFrame = Frame(self._occupiedFrame)
        askFrame.pack()
        occupiedArea = Frame(self._occupiedFrame)
        v=StringVar(value=self._occupiedFile)

        def askFile():
            path = filedialog.askopenfilename(initialdir=v,
                                                            title="选择文件",
                                                            filetypes=(("TIFF 文件", "*.tif"),))
            v.set(path)
            self._occupiedFile=v.get()


        boolVar = BooleanVar()
        def changeOccupiedArea():
            value = boolVar.get()
            self._ifHaveOccupiedArea=value
            if value:
                occupiedArea.pack()
            else:
                occupiedArea.pack_forget()

        askLabel = Label(askFrame,text = "是否需要输入不改变的区域：")

        radioTrue = Radiobutton(askFrame, text='是',value=True, command=changeOccupiedArea,
                                indicatoron=1,variable = boolVar)
        radioFalse = Radiobutton(askFrame, text='否',value=False, command=changeOccupiedArea,
                                indicatoron=1,variable = boolVar)
        boolVar.set(False)
        askLabel.pack(side=LEFT)
        radioTrue.pack(side=LEFT)
        radioFalse.pack(side=LEFT)


        occupiedLabel = Label(occupiedArea, text="不改变的区域（tif文件读取）：")
        occupiedEntry = Entry(occupiedArea, name="occupied", textvariable=v)
        occupiedSelectButton = Button(occupiedArea, text="选择文件",
                                    command=askFile)
        fileTypeFrame = Frame(occupiedArea)
        fileTypeFrame.grid(row=1,column=0,columnspan=3)
        # make sure file type values
        Label(fileTypeFrame,text = "请确定土地类型值是否对应正确").grid(row=0,column=0,columnspan=12)
        i=0
        for objective,value in self._fileTypeMaps.items():
            Label(fileTypeFrame,text=objective).grid(row=1,column=i*2)
            e=Entry(fileTypeFrame,width=5)
            e.grid(row=1,column=i*2+1)
            e.insert(0,value)
            self._fileTypeEntries.append((objective,e))
            i+=1
        self._showOccupiedNumArea = Frame(occupiedArea)
        def readTIF():
            self._occupiedFile = v.get()
            for tuple in self._fileTypeEntries:
                name=tuple[0]
                frame=tuple[1]
                valid,value = self._validateFileType(name,frame)
                if valid:
                    self._fileTypeMaps[name]=value
                else:
                    return False
            self._readTIFfiles()
        Button(self._showOccupiedNumArea,text="计算占用的数值",command=readTIF).pack()
        alertLabel = Label(occupiedArea, text="请保证您读取的文件路径中仅存在英文，不可有中文和空格\n"
                                                    "文件中0值代表可以改变的区域，其他值对应相应土地类型",
                           fg="red")
        occupiedLabel.grid(row=0,column=0)
        occupiedEntry.grid(row=0,column=1)
        occupiedSelectButton.grid(row=0,column=2)
        self._showOccupiedNumArea.grid(row=2,column=0,columnspan=3)
        alertLabel.grid(row=3,column=0,columnspan=3)
    def createExecutionArea(self):
        self._excutionArea = Frame(self._root)
        self._excutionArea.pack()
        #todo add command
        startButton = Button(self._excutionArea,text = "执行",command = self._executeABC)
        stopButton = Button(self._excutionArea, text="停止",command = self._stopABC)
        startButton.pack(side = LEFT)
        stopButton.pack(side=RIGHT)


    def _executeABC(self):
        # self._executionProcess = ABCThread(self._args)
        # self._executionProcess.start()
        if self._getArguments():
            print(self._args)
            # pass
            self._executionProcess = ABCProcess(self._args,self._outputPath)
            self._executionProcess.start()


    def _getArguments(self):
        Input_fragments=[self._compusoryArea,self._optionalArea,self._excutionArea]

        for name,entry in self._entries.items():
            vaild,value = self._validate(entry,name)
            if vaild:
                if name == "outputPath":
                    self._outputPath=value
                else:
                    pos = Interface.PARAM_KEY_TEMPLATE.index(name)
                    self._args[pos]=value
            else:
                return False
        landTypes = {}
        for frame in self._landTypes:
            valid,value = self._validateLandtype(frame)
            if valid:
                landTypes[value[0]]=value[1:]
            else:
                return False
        pos = Interface.PARAM_KEY_TEMPLATE.index("landType_thr")
        self._args[pos]=landTypes
        if self._ifHaveOccupiedArea:
            for tuple in self._fileTypeEntries:
                name=tuple[0]
                frame=tuple[1]
                valid,value = self._validateFileType(name,frame)
                if valid:
                    self._fileTypeMaps[name]=value
                else:
                    return False
        return True

    def _validate(self,entry,name):
        value = entry.get().strip()
        if entry is self._entries["mutate_per"]:
            try:
                value = float(value)
                if not(value>=0.0 and value<=1.0):
                    self.popup("%s栏输入应在0到1之间" % (name))
                    return False,None
            except:
                self.popup("%s栏输入应为小数" % (name))
                return False,None
        elif entry in [self._entries["row"],self._entries["col"],self._entries["dim"]]:
            if value == "":
                self.popup("%s栏输入没有值"%(name))
                return False,None
            try:
                value = int(value)
            except:
                self.popup("%s栏输入应为整数" % (name))
                return False,None
        elif entry in [self._entries["outputPath"],self._entries["readFile"]]:
            if value=="":
                self.popup("输出文件没有值")
                return False,None
        else:
            try:
                value=int(value)
            except:
                self.popup("%s栏输入应为整数" % (name))
                return False,None
        return True,value

    def _validateLandtype(self,frame):
        name = frame._nametowidget("typeEntry0").get().strip()
        lower = frame._nametowidget("typeEntry1").get().strip()
        higher = frame._nametowidget("typeEntry2").get().strip()
        if name == "" or lower == "" or higher == "":
            self.popup("请检查土地种类输入值")
            return False,None
        try:
            lower = int(lower)
            higher = int(higher)
        except:
            self.popup("土地种类上下限应为整数")
            return False,None
        return True,[name,lower,higher]

    def _validateFileType(self,name,frame):
        value = frame.get().strip()
        if value == "":
            self.popup("%s没有输入值"%name)
            return False,None
        try:
            value=int(value)
        except:
            self.popup("%s应为整数"%name)
            return False,None
        return True,value

    def popup(self,msg):
        dialog = Toplevel(self._root,padx = 20, pady = 10)
        x = self._root.winfo_x() + 300
        y = self._root.winfo_y() + 250
        dialog.geometry("280x150+%d+%d" % (x, y))
        dialog.title("输入错误!")

        label = Label(dialog,text = msg)
        B = Button(dialog,text = "ok",command = dialog.destroy,width = 7)
        label.pack(side = TOP,pady = 10)
        B.pack(side=BOTTOM)


    def _stopABC(self):
        if self._executionProcess !=None:

            self._executionProcess.terminate()
            self._executionProcess=None
    def createShowArea(self):
        self._showFrame = Frame(self._root)
        self._showFrame.pack(fill=BOTH)
        showText = Text(self._showFrame, height=10, state=DISABLED)
        showText.pack()
        scroll = Scrollbar(self._showFrame, command=showText.yview)
        showText.configure(yscrollcommand=scroll.set)

    def _readTIFfiles(self):
        CheckProcess(self._occupiedFile,self._fileTypeMaps,self).start()

    def updateLandTypeNums(self,result):
        for child in self._showOccupiedNumArea.winfo_children():
            if isinstance(child,Label):
                child.pack_forget()
        for type,num in result.items():
            Label(self._showOccupiedNumArea,text="%s: %s"%(type,len(num))).pack(side=LEFT)
        pos = Interface.PARAM_KEY_TEMPLATE.index("occupied")
        self._args[pos]=result

class ABCProcess(Process):
    def __init__(self,args,outputPath):
        Process.__init__(self)
        self._args=args
        self._outputPath=outputPath
    def run(self):
        model = BeeHive(*self._args)
        archive = model.run()
        model.writeToFile(self._outputPath)
        dataSet = []
        for bee in archive:
            if len(dataSet) == 0:
                for v in bee.vector:
                    dataSet.append([v])
            else:
                for i, v in enumerate(bee.vector):
                    dataSet[i].append(v)
        exhibit.show(dataSet)

class CheckProcess(Thread):
    def __init__(self,path,landTypeMap,interface):
        Thread.__init__(self)
        self._path=path
        self._landTypeMap = self.switch(landTypeMap)
        self._result={}
        self._interface=interface
    def run(self):
        reader= readTIFgraph.Reader(self._path)
        graph= reader.getFile()
        for r,row in enumerate(graph):
            for c,col in enumerate(row):
                if col == 0 or col not in self._landTypeMap:
                    continue
                type = self._landTypeMap[col]
                if type in self._result:
                    self._result[type].append((r,c))
                else:
                    self._result[type]=[(r,c)]
        self._interface.updateLandTypeNums(self._result)

    def switch(self,old):
        new={}
        for k,v in old.items():
            new[v]=k
        return new







if __name__ == "__main__":
    root = Tk()
    interface = Interface(root)
    root.mainloop()