from tkinter import *
class Interface():
    def __init__(self,root):
        self._root = root
        self._verbose= True
        self.setWindow()
        self.createWedgets()
        # self._compusoryArea.nametowidget("row")["bg"]="green"
    def setWindow(self):
        self._root.title('土地分配优化')
        self._root.geometry('640x480')
        self._root.resizable(width=True, height=True)
    def createWedgets(self):
        self.createCompusoryArea()
        self.createOptionalArea()

    def createCompusoryArea(self):
        self._compusoryArea = Frame(self._root)
        self._compusoryArea.pack()
        rowLabel = Label(self._compusoryArea, text="输入输出行数")
        rowEntry = Entry(self._compusoryArea, name="row")
        colLabel = Label(self._compusoryArea, text="输入输出列数")
        colEntry = Entry(self._compusoryArea, name="col")
        dimLabel = Label(self._compusoryArea, text="指标个数")
        dimEntry = Entry(self._compusoryArea, name="dim")
        print(rowLabel)
        rowLabel.grid(row=0, column=0)
        rowEntry.grid(row=0, column=1)

        colLabel.grid(row=1, column=0)
        colEntry.grid(row=1, column=1)

        dimLabel.grid(row=2, column=0)
        dimEntry.grid(row=2, column=1)

    def createOptionalArea(self):
        def changeVerbose(boolValue):
            self._verbose = boolValue

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










if __name__ == "__main__":
    root = Tk()
    interface = Interface(root)
    root.mainloop()