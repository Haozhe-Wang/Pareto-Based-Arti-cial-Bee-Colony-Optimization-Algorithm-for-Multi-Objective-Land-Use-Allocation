from tkinter import *
from ABCalgorithm import *
import time
import exhibit
from multiprocessing import Process
class Interface():
    PARAM_KEY_TEMPLATE = ["row","col","dim","occupied","numb_bees","landType_thr",
                            "max_itrs","max_trials","max_PA","max_FS","mutate_per","verbose"]
    def __init__(self,root):
        self._root = root

        self._verbose= True
        self._executionProcess = None
        self._args = [None, None, None, None, 30, None, 100, 40, 100, 20, 0.3, True]
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
        self.createExecutionArea()
        self.createLandTypeInputArea()
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
        self._entries["row"]=rowEntry
        self._entries["col"] = colEntry
        self._entries["dim"] = dimEntry
        rowLabel.grid(row=0, column=0)
        rowEntry.grid(row=0, column=1)

        colLabel.grid(row=1, column=0)
        colEntry.grid(row=1, column=1)

        dimLabel.grid(row=2, column=0)
        dimEntry.grid(row=2, column=1)

    def createOptionalArea(self):
        def changeVerbose(boolValue):
            self._verbose = boolValue
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

        self._entries["numb_bees"] = numBeeEntry
        self._entries["max_itrs"] = maxIterEntry
        self._entries["max_PA"] = maxPAEntry
        self._entries["max_FS"] = foodSourceEntry
        self._entries["mutate_per"] = mutatePerEntry

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

        verboseLabel = Label(self._optionalArea,text = "是否展示计算过程")
        verboseFrame = Frame(self._optionalArea)
        radioTrue = Radiobutton(verboseFrame, text='True', command=lambda: changeVerbose(True),
                                indicatoron=0)
        radioFalse = Radiobutton(verboseFrame, text='False',value=False, command=lambda: changeVerbose(False),
                                 indicatoron=0)
        radioTrue.pack(side=LEFT)
        radioFalse.pack(side=RIGHT)
        verboseLabel.grid(row=5,column=0)
        verboseFrame.grid(row=5,column=1)

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
            pass
            # self._executionProcess = ABCProcess(self._args)
            # self._executionProcess.start()


    def _getArguments(self):
        Input_fragments=[self._compusoryArea,self._optionalArea,self._excutionArea]

        for name,entry in self._entries.items():
            vaild,value = self._validate(entry,name)
            if vaild:
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


class ABCProcess(Process):
    def __init__(self,args):
        Process.__init__(self)
        self._args=args
    def run(self):
        model = BeeHive(*self._args)
        archive = model.run()
        # model.writeToFile("solutions.txt")
        dataSet = []
        for bee in archive:
            if len(dataSet) == 0:
                for v in bee.vector:
                    dataSet.append([v])
            else:
                for i, v in enumerate(bee.vector):
                    dataSet[i].append(v)
        exhibit.show(dataSet)









if __name__ == "__main__":
    root = Tk()
    interface = Interface(root)
    root.mainloop()