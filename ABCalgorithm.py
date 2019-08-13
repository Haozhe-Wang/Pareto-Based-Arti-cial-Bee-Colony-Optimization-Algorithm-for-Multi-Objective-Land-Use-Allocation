#!/usr/bin/env python

import random
import sys
import copy
import math
import numpy
import logging
from implementation.GenerateRandomData import printMatrix,getMatrix
from implementation.readInformation import readInformation


# ---- BEE CLASS

class Bee(object):
    """ Creates a bee object. """

    def __init__(self, matrix, landType_thr,funcon=None):
        """

        Instantiates a bee object randomly.

        Parameters:
        ----------
            :param dict landType_thr  :  the threshold of the number of each land type
            :param def  funcon : constraints function, must return a boolean


        """
        self._vector = []
        assert type(matrix)==list
        self._matrix = matrix
        self._fitness = sys.float_info.max
        self._landType_thr = landType_thr
        # self._pos_lookUp={}
        # self.initPosLookUp()
        # initialises trial limit counter - i.e. abandonment counter
        self._counter = 0
        #todo add 0 type representing the cell will not be used

        self.calculateVector()

        # checks if the problem constraint(s) are satisfied
        # TODO: can write a constrain function, i.e. checking the limit of the number of certain type
        if not funcon:
            self.valid = True
        else:
            self.valid = funcon(self._vector)

        '''
        # computes fitness of solution vector
        #TODO: change the function to compute the fitness
        #TODO: this time, fitness may a list of values(vector) in different direction
        if (fun != None):
            self.value = fun(self._vector)
        else:
            self.value = sys.float_info.max
        '''

    def calculateVector(self):
        #todo: this should be replaced by model function(得到各种类型在不同栅格的指标是多少）
        #必须返回 dict 类型 --> key：土地类型（例：森林） value：矩阵（每个栅格对应这个类型的各个指标）
        info = readInformation(list(self._landType_thr.keys()))
        self._vector=self._calculateVector(info)

    def _calculateVector(self,info):
        """
        :param info: information of each cell corresponding each objective
        :param matrix: the solution matrix
        :return:
        """
        vector = []
        for row in range(len(self._matrix)):
            for col in range(len(self._matrix[row])):
                type = self._matrix[row][col]
                value = info[type][row][col]
                # self._pos_lookUp[type].append((row,col))
                if vector == []:
                    vector = value
                    continue
                else:
                    for i in range(len(value)):
                        vector[i] += value[i]
        return vector
    # def initPosLookUp(self):
    #     for type in self._landType_thr.keys():
    #         self._pos_lookUp[type]=[]
    def getVector(self):
        return self._vector
    def setMatrix(self,matrix):
        assert type(matrix) == list
        self._matrix=matrix
        # self.initPosLookUp()
        self.calculateVector()
    def getMatrix(self):
        return self._matrix
    def setFitness(self,fitness):
        # fitness is actually crowding distance
        self._fitness = fitness
    def getFitness(self):
        return self._fitness
    def getCounter(self):
        return self._counter
    def incCounter(self,counter):
        self._counter+=1
    def __str__(self):
        output=""
        output+=getMatrix(self.matrix)
        output+="\n%s"%self._vector
        return output
    fitness= property(getFitness,setFitness)
    vector=property(getVector)
    matrix = property(getMatrix,setMatrix)
    counter=property(getCounter)

class BeeHive(object):
    """

    Creates an Artificial Bee Colony (ABC) algorithm.

    The food_source of the hive is composed of three distinct types
    of individuals:

        1. "employees",
        2. "onlookers",
        3. "scouts".

    The employed bees and onlooker bees exploit the nectar
    sources around the hive - i.e. exploitation phase - while the
    scouts explore the solution domain - i.e. exploration phase.

    The number of nectar sources around the hive is equal to
    the number of actively employed bees and the number of employees
    is equal to the number of onlooker bees.

    """
    def run(self):
        """ Runs an Artificial Bee Colony (ABC) algorithm. """

        for itr in range(self.max_itrs):

            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S')
            logging.info("print")
            # creates a bee hive
            self.food_source = [Bee(self.randomGeneration(), self._landType_thr) for i in range(self.size)]
            # employees phase
            for index in range(self.size):
                self.send_employee(index)
            self.trim(self.food_source,self._maxFS)

            # onlookers phase
            self.send_onlookers()

            # scouts phase
            self.send_scout()

            self._paretoArchive+=self.food_source
            self.trim(self._paretoArchive,self._maxPA)

            # prints out information about computation
            if self.verbose:
                self._verbose(itr)

        return self._paretoArchive

    def __init__(self                 ,
                 row                  ,
                 col                  ,
                 value_constrain       ,
                 numb_bees    =  30   ,
                 landType_thr = None     ,
                 max_itrs     = 100   ,
                 max_trials   = None  ,
                 max_PA       =  100 ,
                 max_FS       =   20,
                 mutate_per   = 0.3   ,
                 selfun       = None  ,
                 verbose      = False ,
                 extra_params = None ,):
        """

        Instantiates a bee hive object.

        1. INITIALISATION PHASE.
        -----------------------

        The initial food_source of bees should cover the entire search space as
        much as possible by randomizing individuals within the search
        space constrained by the prescribed lower and upper bounds.

        Parameters:
        ----------
            :param int row             : number of rows of the solution
            :param int col             : number of columns of the solution
            :param dict value_constrain: constrain of solution vector for each value
            :param int numb_bees       : number of active bees within the hive
            :param dict landType_thr   : threshold of each land type numbers
            :param int max_trials      : max number of trials without any improvment
            :param int max_PA          : max capacity of pareto archive
            :param int max_FS          : max capacity of food source
            :param def selfun          : custom selection function
            :param float mutate_per    : percentage of cells will be exchanged in mutation phrase
            :param boolean verbose     : makes computation verbose
            :param dict extra_params   : optional extra arguments for selection function selfun

        """
        self._paretoArchive = []
        self._row = row
        self._random_maximum_times=10
        self._col = col
        self._maxPA = max_PA
        self._maxFS = max_FS
        self._landType_thr = landType_thr #the min and max number of cells of each type can be allocated
        self._mutatePer=mutate_per
        self.verbose = verbose
        #todo need new function to determine dominance

        # computes the number of employees
        self.size = numb_bees //2

        # assigns properties of algorithm
        # dimension
        self.dim = len(value_constrain)
        self.max_itrs = max_itrs

        #TODO this can be changed
        # max number of trials without any improvement
        # later, there will be a counter for each bee, counting the number of trials without any improvements
        if (max_trials == None):
            self.max_trials = 0.6 * self.size * self.dim
        else:
            self.max_trials = max_trials

        # TODO: can be replaced with self defined function
        # selfun --> computes the probability(of the employed bee share to the onlooker bees)
        self.selfun = selfun
        # the parameters used in selfun
        self.extra_params = extra_params

        # # assigns properties of the optimisation problem
        # self.evaluate = fun
        self._value_constrain    = value_constrain

    def trim(self,collection,maxNum):
        result=[]
        index=0
        def getValue(arg):
            return arg.fitness
        while index<len(collection):
            ifAppend = True
            for k in range(len(collection)):
                if index != k:
                    ifIsDominated,canDecide = self.ifDominated(collection[index],collection[k])
                    if ifIsDominated==True:
                        collection.pop(index)
                        index-=1
                        ifAppend=False
                        break
            if ifAppend:
                result.append(collection[index])
            index+=1
        if len(result)>maxNum:
            for bee in result:
                bee.fitness=self.fitness(bee,collection)
            result=sorted(result,key=lambda arg: getValue(arg),reverse=True)
            result=result[:maxNum]
        return result


    def compute_probability(self):
        """

        Computes the relative chance that a given solution vector is
        chosen by an onlooker bee after the Waggle dance ceremony when
        employed bees are back within the hive.

        """
        total = 0
        probabilities=[]
        for bee in self.food_source:
            temp=self.fitness(bee,self.food_source)
            bee.fitness=temp
            total+=temp
        for bee in self.food_source:
            probability = bee.fitness/total
            probabilities.append((probability,bee))
        return probabilities

    def send_employee(self, index):

        # deepcopies current bee solution vector
        zombee = copy.deepcopy(self.food_source[index])

        # produces a mutant based on current bee and bee's friend
        newSolutions = self.mutateAndCrossover(zombee,index)
        self.food_source+=newSolutions

    def send_onlookers(self):
        # evaluate fitness in food source
        numb_onlookers = 0; beta = 0
        for bee in self.food_source:
            bee.fitness=self.fitness(bee,self.food_source)
        while (numb_onlookers < self.size):

            # selects a new onlooker based on waggle dance
            #Use roulette wheel strategy
            index = self.select()

            # sends new onlooker
            self.send_employee(index)
            self.trim(self.food_source,self._maxFS)

            # increments number of onlookers
            numb_onlookers += 1

    def select(self):


        # computes probability intervals "online" - i.e. re-computed after each onlooker
        probas = self.compute_probability()
        beta = random.random()
        accumulator = 0
        for index,proba in enumerate(probas):
            if numpy.isnan(proba[0]):
                accumulator+=0
            else:
                accumulator+=proba[0]
            if (beta < accumulator):
                assert self.food_source[index] == proba[1]
                return index
        return 0

    def send_scout(self):
        """
        Identifies bees whose abandonment counts exceed preset trials limit,
        abandons it and creates a new random bee to explore new random area
        of the domain space.

        """

        # retrieves the number of trials for all bees
        trials = [ (self.food_source[i].counter,i) for i in range(len(self.food_source)) ]
        trials.sort(reverse=True)

        for trial in trials:
            # checks if its number of trials exceeds the pre-set maximum number of trials
            if (trial[0] > self.max_trials):

                index = trial[1]
                # creates a new scout bee randomly
                self.food_source[index] = Bee(self.randomGeneration(),self._landType_thr)

                # sends scout bee to exploit its solution vector
                self.send_employee(index)
            else:
                break
        self.trim(self.food_source,self._maxFS)


    def _check(self, matrix):
        """

        Checks that a solution vector is contained within the
        pre-determined lower and upper bounds of the problem.

        """

        valid = True
        violates = {}
        for r in range(self._row):
            for c in range(self._col):
                type =matrix[r][c]
                if type in violates.keys():
                    violates[type]+=1
                else:
                    violates[type]=0
        for name,threshold in self._landType_thr.items():
            if name not in violates:
                violates[name]=0
            low_thr = threshold[0]
            num = violates[name]
            if num - low_thr>=0:
                high_thr = threshold[1]
                # high_thr <0 means the number of the type has no upper threshold
                if high_thr<0 or high_thr-num >= 0:
                    del violates[name]
                else:
                    violates[name]= num - high_thr # the number of cells that exceed the upper threshold
            else:
                violates[name]=num-low_thr # the number of cells that less than the lower threshold
        if len(violates)>0:
            valid=False
        return valid,violates

    def _adjust(self,matrix, violates):
        # the adjust function may be changed as needed
        pos_lookUp=self.posLookUp(matrix)
        low_list = []
        high_list=[]
        normal_list = list(self._landType_thr.keys())
        for type,diff in violates.items():
            if diff > 0:
                high_list.append(type)
            else:
                low_list.append(type)
            normal_list.remove(type)
        for low in low_list:
            while violates[low]<0:
                select_poss=[]
                selected_type=""
                while select_poss == []:
                    if len(high_list)>0:
                        index = random.randint(0,len(high_list)-1)
                        selected_type = high_list[index]
                    else:
                        index = random.randint(0, len(normal_list) - 1)
                        selected_type = normal_list[index]
                    # random select a position for each type
                    select_poss = pos_lookUp[selected_type]
                    # make sure the selected type is able to decrease its amount
                    if not len(select_poss)>self._landType_thr[selected_type][0]:
                        select_poss=[]

                select_index = random.randint(0, len(select_poss) - 1)
                select_pos = select_poss[select_index]

                # replace selected value
                matrix[select_pos[0]][select_pos[1]]=low
                pos_lookUp[low].append(select_pos)
                pos_lookUp[selected_type].pop(select_index)
                violates[low]+=1
                # if selected type is the type needed to be reduced
                if selected_type in high_list:
                    violates[selected_type]-=1
                    if not violates[selected_type]>0:
                        high_list.remove(selected_type)
                        normal_list.append(selected_type)

            # del violates[low]
            normal_list.append(low)
        logging.info(4)
        for high in high_list:
            while violates[high]>0:
                selected_type=""
                while selected_type=="" or (self._landType_thr[selected_type][1] != -1 and
                    (not len(pos_lookUp[selected_type])<self._landType_thr[selected_type][1])):
                    #random select a type to replace the high  type
                    index = random.randint(0, len(normal_list) - 1)
                    selected_type = normal_list[index]
                    print(selected_type,index,len(pos_lookUp[selected_type]),self._landType_thr[selected_type][1])
                # random select a position in high list positions
                high_poss = pos_lookUp[high]
                high_index = random.randint(0,len(high_poss)-1)
                high_pos = high_poss[high_index]

                #replace the position with another type
                matrix[high_pos[0]][high_pos[1]] = selected_type
                pos_lookUp[selected_type].append(high_pos)
                pos_lookUp[high].pop(high_index)
                violates[high] -= 1

        return matrix
    def adjustMatrix(self,matrix):
        valid, violates = self._check(matrix)
        logging.info(2)
        if not valid:
            logging.info(3)
            matrix = self._adjust(matrix, violates)
        return matrix

    def _verbose(self, itr):
        print("*"*100)
        print("*"*100)
        print("******* iteration: %s  *******"%itr)
        for bee in self._paretoArchive:
            print(bee)
            print("\n"+"-"*100+"\n")

    @staticmethod
    def getVector(bee, index):
        """
        get the objective to be sorted
        :param bee: the object contains the vector and matrix
        :param index: the index to be sorted
        """
        return bee.vector[index]
    def fitness(self,target_bee,collection):
        """
        compute the fitness base on crowding distance
        :param list collection: can be pareto archive or food source(list of bee objects)
        """


        sum_distance = 0
        num_set = len(collection)
        for n in range(self.dim):
            # ascending sort
            set = sorted(collection,key=lambda arg:BeeHive.getVector(arg,n))
            target_i = set.index(target_bee)
            max_obj = set[-1]
            min_obj = set[0]

            '''max_vector=[]
            min_vector=[]
            target_i=0
            num_set= len(set)
            for i in range(len(set)):
                if i == 0:
                    max_vector=set[0].vector
                    min_vector=set[num_set-1].vector
                else:
                    temp_vector = set[i].vector
                    for num in range(len(temp_vector)):
                        if temp_vector[num] > max_vector[num]:
                            max_vector[num]=temp_vector[num]
                        if temp_vector[num]<min_vector[num]:
                            min_vector[num]=temp_vector[num]
                if set[i] == target_bee:
                    target_i=i'''

            if target_i>0 and target_i<num_set-1:
                neighbor_less = set[target_i-1].vector[n]
                neighbor_high = set[target_i+1].vector[n]

                dividend = math.fabs(neighbor_high-neighbor_less)
                divisor = max_obj.vector[n]-min_obj.vector[n]
                sum_distance+=dividend/divisor
            else:
                sum_distance+=sys.float_info.max

        return sum_distance
    def randomGeneration(self):
        """ Initialises a solution vector randomly. """

        #todo: can be changed to another way to generate the matrix!!!
        # generate the number of each land type based on criteria
        num_landType = {}
        landTypes = []
        num_rasterCell= self._row * self._col
        matrix = [[None] * self._col for i in range(self._row)]
        for name,threshold in self._landType_thr.items():
            if threshold[0]<=0:
                num_landType[name]=0
            else:
                num_landType[name]=threshold[0]
                num_rasterCell-=threshold[0]
                assert num_rasterCell>=0
            landTypes.append(name)
        while num_rasterCell>0:
            num = random.randint(0,len(landTypes)-1)
            if num_landType[landTypes[num]] < self._landType_thr[landTypes[num]][1]:
                # if number of land types smaller than its upper threshold
                num_landType[landTypes[num]]+=1
                num_rasterCell-=1
            elif self._landType_thr[landTypes[num]][1]<0:
                num_landType[landTypes[num]] += 1
                num_rasterCell -= 1
            else:
                landTypes.pop(num)
        landTypes=list(self._landType_thr.keys())
        for r in range(self._row):
            for c in range(self._col):
                while 1:
                    num=random.randint(0,len(landTypes)-1)
                    if num_landType[landTypes[num]] > 0:
                        # if number of land types can be assigned
                        matrix[r][c]=landTypes[num]
                        num_landType[landTypes[num]] -= 1
                        break
                    else:
                        landTypes.pop(num)
        printMatrix(matrix)
        return matrix
    def mutateAndCrossover(self,bee,index):
        bee_ix = index
        if len(self.food_source) == 1:
            return [self._mutate(copy.deepcopy(bee))]
        while (bee_ix == index):
            bee_ix = random.randint(0, len(self.food_source)-1)
        return self._mutateAndCrossover(copy.deepcopy(bee),copy.deepcopy(self.food_source[bee_ix]))
    def _mutateAndCrossover(self,bee,otherBee):
        newBee=self._mutate(bee)
        logging.info(-1)
        newBee = self.chooseBetterSolutionBee(bee,newBee)
        logging.info(0)
        newBee1,newBee2 =self._crossover(newBee,otherBee)
        logging.info("print2")
        return [newBee1,newBee2]


    def _randomGetCell(self):
        row = random.randint(0, self._row - 1)
        col = random.randint(0, self._col - 1)
        return row, col
    def _mutate(self,bee):
        """

        :param bee: the bee object with matrix to be mutated
        :return: a bee object with new matrix
        """
        num_cell = int(self._row * self._col*self._mutatePer)
        matrix = bee.matrix
        for i in range(num_cell):
            row1,row2,col1,col2=0,0,0,0
            # only iterate to maximum of 10 times, in case of extreme conditions making the program running infinitely
            for i in range(self._random_maximum_times):
                row1,col1 = self._randomGetCell()
                row2,col2 = self._randomGetCell()
                if not (row1==row2 and col1 == col2):
                    break
            matrix[row1][col1],matrix[row2][col2]=matrix[row2][col2],matrix[row1][col1]
        bee.matrix=matrix
        return bee

    def _crossover(self,bee,otherBee):
        matrix = bee.matrix
        otherMatrix = otherBee.matrix
        landTypes = list(self._landType_thr.keys())
        num_landTypes = len(landTypes)
        RM = [[None]*num_landTypes for i in range(num_landTypes)]
        for r in range(num_landTypes):
            for c in range(num_landTypes):
                if r!=c:
                    RM[r][c]=random.randint(0,1)
                else:
                    RM[r][c] =0
        pos_lookup={}
        for i,landType in enumerate(landTypes):
            pos_lookup[landType]=i
        for r in range(self._row):
            for c in range(self._col):
                type1 = pos_lookup[matrix[r][c]]
                type2 = pos_lookup[otherMatrix[r][c]]
                ifChange = RM[type1][type2]
                if ifChange == 1:
                    matrix[r][c],otherMatrix[r][c]=otherMatrix[r][c],matrix[r][c]
        logging.info(1)
        bee.matrix=self.adjustMatrix(matrix)
        otherBee.matrix=self.adjustMatrix(otherMatrix)
        return [bee,otherBee]
    def ifDominated(self,bee,otherBee):
        """
        todo may change the implementation of dominance juedgement
        :return: boolean. True: bee is dominated by otherBee,
                  boolean  True: if we can decide which solution is better
        """
        vector = bee.vector
        otherVector= otherBee.vector
        haveGreater = False
        haveLess = False
        for i in range(len(vector)):
            if vector[i]>otherVector[i]:
                haveLess = True
            if vector[i]<otherVector[i]:
                haveGreater=True
        if haveGreater and not haveLess:
            return True,True
        elif haveLess and not haveGreater:
            return False,True
        else:
            # if all objective function returns equivalent value
            # or if some objective function is better while others are not
            return False,False

    def compromisingPrograming(self,bee,otherBee):
        """
        This is used to compare two bees using weighted sum
        the calculation see reference page 8
        weight = (f(x) - f(min))/(f(max)-f(min))
        :return: Bee the better bee is selected, if equal, select bee
        """
        vector = bee.vector
        otherVector= otherBee.vector
        max_vectors = []
        min_vectors = []
        for n in range(self.dim):
            set = sorted(self.food_source, key=lambda arg: BeeHive.getVector(arg, n))
            min_vectors.append(set[0].vector[n])
            max_vectors.append(set[-1].vector[n])
        vector_weight = 0
        otherVector_weight =0
        for i in range(self.dim):
            min = min_vectors[i]
            max = max_vectors[i]
            vector_weight+=(vector[i]-min)/(max-min)
            otherVector_weight+=(otherVector[i] - min)/(max-min)
        if vector_weight>=otherVector_weight:
            # inc counter?????????????????????????????????????
            return bee
        else:
            return otherBee




    def chooseBetterSolutionBee(self,bee,otherBee):
        """
        choose a bee to be retained from 2 input
        :return: the better bee
        """
        #todo may change the implementation of this function along with ifDominated
        ifDominated, canDecide = self.ifDominated(bee, otherBee)
        if ifDominated:
            return otherBee
        elif not ifDominated and canDecide:
            return bee
        else:
            return self.compromisingPrograming(bee,otherBee)

            #     bee.incCounter()

    def posLookUp(self,matrix):
        pos_lookUp={}
        for type in self._landType_thr:
            pos_lookUp[type]=[]
        for r in range(self._row):
            for c in range(self._col):
                type=matrix[r][c]
                pos_lookUp[type].append((r,c))
        return pos_lookUp




