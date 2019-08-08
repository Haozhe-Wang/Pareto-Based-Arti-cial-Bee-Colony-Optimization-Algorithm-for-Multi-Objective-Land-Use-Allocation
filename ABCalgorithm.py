#!/usr/bin/env python

import random
import sys
import copy
import operator
import math
from implementation.GenerateRandomData import printMatrix
from implementation.readInformation import readInformation


# ---- BEE CLASS
def calculateVector(info,matrix):
    """
    :param info: information of each cell corresponding each objective
    :param matrix: the solution matrix
    :return:
    """
    vector = []
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            type = matrix[row][col]
            value=info[type][row][col]
            if vector == []:
                vector=value
                continue
            else:
                for i in range(len(value)):
                    vector[i]+=value[i]
    return vector
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
        self._matrix = matrix
        self._fitness = sys.float_info.max
        self._landType_thr = landType_thr
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
        self._vector=calculateVector(info,self._matrix)

    def getVector(self):
        return self._vector
    def setMatrix(self,matrix):
        self._matrix=matrix
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

            # employees phase
            for index in range(self.size):
                self.send_employee(index)

            # onlookers phase
            self.send_onlookers()

            # scouts phase
            self.send_scout()

            # computes best path
            self.find_best()

            '''
            # stores convergence information
            cost["best"].append( self.best )
            cost["mean"].append( sum( [ bee.value for bee in self.food_source ] ) / self.size )
            '''


            # prints out information about computation
            if self.verbose:
                self._verbose(itr, cost)

        return cost

    def __init__(self                 ,
                 row                  ,
                 col                  ,
                 value_constrain       ,
                 numb_bees    =  30   ,
                 landType_thr = None     ,
                 max_itrs     = 100   ,
                 max_trials   = None  ,
                 mutate_per   = 0.3   ,
                 crossover_per  = 0.3 ,
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
            :param def selfun          : custom selection function
            :param float mutate_per    : percentage of cells will be exchanged in mutation phrase
            :param float crossover_per : percentage of cells will be exchanged in crossover phrase
            :param boolean verbose     : makes computation verbose
            :param dict extra_params   : optional extra arguments for selection function selfun

        """
        self._paretoArchive = []
        self._row = row
        self._col = col
        self._landType_thr = landType_thr
        self._mutatePer=mutate_per
        self._crossoverPer=crossover_per
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

        '''
        # initialises current best and its a solution vector
        #TODO: may be replaced by new judgement corresponding to matrix
        self.best = sys.float_info.max
        #TODO: maybe replaced to solutions sets(food set)
        self.solution = None
        '''

        # creates a bee hive
        self.food_source = [ Bee(self.randomGeneration(),self._landType_thr) for i in range(self.size) ]
        #
        # # initialises best solution vector to food nectar
        # self.find_best()
        #
        # # computes selection probability
        # self.compute_probability()
        #
        # # verbosity of computation
        # self.verbose = verbose

    def find_best(self):
        """ Finds current best bee candidate. """
        #todo: this is useless, change the function to put all solutions in food source set

        values = [ bee.value for bee in self.food_source ]
        index  = values.index(min(values))
        if (values[index] < self.best):
            self.best     = values[index]
            self.solution = self.food_source[index].vector

    def compute_probability(self):
        """

        Computes the relative chance that a given solution vector is
        chosen by an onlooker bee after the Waggle dance ceremony when
        employed bees are back within the hive.

        """

        # retrieves fitness of bees within the hive
        #todo change here to call bee _fitness function
        values = [bee.fitness for bee in self.food_source]
        max_values = max(values)

        # computes probalities the way Karaboga does in his classic ABC implementation
        if (self.selfun == None):
            self.probas = [0.9 * v / max_values + 0.1 for v in values]
        else:
            if (self.extra_params != None):
                self.probas = self.selfun(list(values), **self.extra_params)
            else:
                self.probas = self.selfun(values)

        # returns intervals of probabilities
        return [sum(self.probas[:i+1]) for i in range(self.size)]

    def send_employee(self, index):
        """

        2. SEND EMPLOYED BEES PHASE.
        ---------------------------

        During this 2nd phase, new candidate solutions are produced for
        each employed bee by cross-over and mutation of the employees.

        If the modified vector of the mutant bee solution is better than
        that of the original bee, the new vector is assigned to the bee.

        """

        # deepcopies current bee solution vector
        zombee = copy.deepcopy(self.food_source[index])

        # selects another bee
        bee_ix = index
        while (bee_ix == index): bee_ix = random.randint(0, self.size-1)

        # produces a mutant based on current bee and bee's friend
        self._mutateAndCrossover(zombee,copy.deepcopy(self.food_source[bee_ix]))

        # computes fitness of mutant
        # todo: change here for fitness invocation
        zombee.value = self.evaluate(zombee.vector)
        zombee._fitness()

        # deterministic crowding
        # todo have a local food set, use weighted sum to compare if necessary
        if (zombee.fitness > self.food_source[index].fitness):
            self.food_source[index] = copy.deepcopy(zombee)
            self.food_source[index].counter = 0
        else:
            self.food_source[index].counter += 1

    def send_onlookers(self):
        """

        3. SEND ONLOOKERS PHASE.
        -----------------------

        We define as many onlooker bees as there are employed bees in
        the hive since onlooker bees will attempt to locally improve the
        solution path of the employed bee they have decided to follow
        after the waggle dance phase.

        If they improve it, they will communicate their findings to the bee
        they initially watched "waggle dancing".

        """

        # sends onlookers
        numb_onlookers = 0; beta = 0
        while (numb_onlookers < self.size):

            # draws a random number from U[0,1]
            phi = random.random()

            # increments roulette wheel parameter beta
            beta += phi * max(self.probas)
            beta %= max(self.probas)

            # selects a new onlooker based on waggle dance
            index = self.select(beta)

            # sends new onlooker
            self.send_employee(index)

            # increments number of onlookers
            numb_onlookers += 1

    def select(self, beta):
        """

        4. WAGGLE DANCE PHASE.
        ---------------------

        During this 4th phase, onlooker bees are recruited using a roulette
        wheel selection.

        This phase represents the "waggle dance" of honey bees (i.e. figure-
        eight dance). By performing this dance, successful foragers
        (i.e. "employed" bees) can share, with other members of the
        colony, information about the direction and distance to patches of
        flowers yielding nectar and pollen, to water sources, or to new
        nest-site locations.

        During the recruitment, the bee colony is re-sampled in order to mostly
        keep, within the hive, the solution vector of employed bees that have a
        good fitness as well as a small number of bees with lower fitnesses to
        enforce diversity.

        Parameter(s):
        ------------
            :param float beta : "roulette wheel selection" parameter - i.e. 0 <= beta <= max(probas)

        """

        # computes probability intervals "online" - i.e. re-computed after each onlooker
        probas = self.compute_probability()

        # selects a new potential "onlooker" bee
        for index in range(self.size):
            if (beta < probas[index]):
                return index

    def send_scout(self):
        """

        5. SEND SCOUT BEE PHASE.
        -----------------------

        Identifies bees whose abandonment counts exceed preset trials limit,
        abandons it and creates a new random bee to explore new random area
        of the domain space.

        In real life, after the depletion of a food nectar source, a bee moves
        on to other food sources.

        By this means, the employed bee which cannot improve their solution
        until the abandonment counter reaches the limit of trials becomes a
        scout bee. Therefore, scout bees in ABC algorithm prevent stagnation
        of employed bee food_source.

        Intuitively, this method provides an easy means to overcome any local
        optima within which a bee may have been trapped.

        """

        # retrieves the number of trials for all bees
        trials = [ self.food_source[i].counter for i in range(self.size) ]

        # identifies the bee with the greatest number of trials
        index = trials.index(max(trials))

        # checks if its number of trials exceeds the pre-set maximum number of trials
        if (trials[index] > self.max_trials):

            # creates a new scout bee randomly
            self.food_source[index] = Bee(self.lower, self.upper, self.evaluate)

            # sends scout bee to exploit its solution vector
            self.send_employee(index)


    def _check(self, vector, dim=None):
        #todo change the checking criteria to matrix
        """

        Checks that a solution vector is contained within the
        pre-determined lower and upper bounds of the problem.

        """

        if (dim == None):
            range_ = range(self.dim)
        else:
            range_ = [dim]

        for i in range_:

            # checks lower bound
            if  (vector[i] < self.lower[i]):
                vector[i] = self.lower[i]

            # checks upper bound
            elif (vector[i] > self.upper[i]):
                vector[i] = self.upper[i]

        return vector

    def _verbose(self, itr, cost):
        """ Displays information about computation.
         todo change the way printing the information
         """


        msg = "# Iter = {} | Best Evaluation Value = {} | Mean Evaluation Value = {} "
        print(msg.format(int(itr), cost["best"][itr], cost["mean"][itr]))

    def fitness(self,target_bee,collection):
        """
        compute the fitness base on crowding distance
        :param list collection: can be pareto archive or food source(list of bee objects)
        """

        def getVector(bee,index):
            """
            get the objective to be sorted
            :param bee: the object contains the vector and matrix
            :param index: the index to be sorted
            :return:
            """
            return bee.vector[index]
        sum_distance = 0
        num_set = len(collection)
        for n in range(self.dim):
            # ascending sort
            set = sorted(collection,key=lambda arg:getVector(arg,n))
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
                divisor = max_obj[n]-min_obj[n]
                sum_distance+=dividend/divisor
            else:
                sum_distance+=sys.float_info.max
        target_bee.fitness=sum_distance
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
    def _mutateAndCrossover(self,bee,otherBee):
        newBee=self._mutate(bee)
        ifDominated =self.ifDominated(bee,newBee)
        if not ifDominated:
            bee.incCounter()
        self._crossover(bee,otherBee)

    def _mutate(self,bee):
        def randomGetCell():
            row = random.randint(0, self._row - 1)
            col = random.randint(0, self._col-1)
            return row,col
        num_cell = int(self._row * self._col*self._mutatePer)
        matrix = bee.matrix
        for i in range(num_cell):
            row1,row2,col1,col2=0,0,0,0
            while 1:
                row1,col1 = randomGetCell()
                row2.col2 = randomGetCell()
                if not (row1==row2 and col1 == col2):
                    break
            matrix[row1][col1],matrix[row2][col2]=matrix[row2][col2],matrix[row1][col1]
        bee.matrix=matrix
        return bee


    def _crossover(self,bee,otherBee):
        # checks boundaries
        # todo change here to check the value
        bee.vector = self._check(bee.vector)
    def ifDominated(self,bee,otherBee):
        """
        :return: boolean. True: bee is dominated by otherBee
        """
        vector = bee.vector
        otherVector= otherBee.vector
        haveGreater = False
        for i in range(len(vector)):
            if vector[i]>otherVector[i]:
                return False
            if vector[i]<otherVector[i]:
                haveGreater=True
        return haveGreater




