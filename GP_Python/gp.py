from __future__ import annotations
from gpTree import Tree
from gpNode import Node
import random

class GeneticProgram:
    population:list[Tree] = []
    aptitudes:list = None
    bestAptitud = -9999
    bestParent = None
    #problem in Tree.evaluate tree
    #TODO: suspected problem in copy tree
    def __init__(self, popSize, maxGen, maxDepth, treeType, pm) -> None:
        """ popsize: population size
            maxGen: Maximum amount of generations
            maxDepth: max depth for the trees in population
            treeType: tree type, full or grow
            pm: probability of mutation
        """
        #generate random population of size popSize
        self.initialPopulation(popSize,maxDepth,treeType)
        print(self.population)
        #may implement generation without improvement
        self.showPopulation()
        for i in range(maxGen):
            # self.showPopulation()
            #evaluate individuals
            self.getAptitudes()
            #select parents
            parents = self.parentSelection(popSize, self.aptitudes,'torneo')
            #cross
            print(parents)
            offspring:list[Tree] = []
            for i in range(0,popSize,2):
                parent1 = self.population[parents[i]]
                parent2= self.population[parents[i+1]]
                # print(parent1,i)
                # print(parent2,i+1)
                newOffspring1, newOffspring2 = self.__cross(parent1, parent2)
                offspring.append(newOffspring1)
                offspring.append(newOffspring2)
            #will use generational selection for the moment
            self.population = offspring
            #mutate
            for individual in self.population:
                individual.mutate(pm)
        print(self.population)
        
            
            
    def initialPopulation(self, popSize,maxDepth,treeType):
        #Generate random population
        self.aptitudes = [None]*popSize
        if treeType == "full":
            for i in range(popSize):
                self.population.append(Tree())
                self.population[i].createTreeFull(maxDepth)
        else:
            for i in range(popSize):
                self.population.append(Tree())
                self.population[i].createTreeGrow(maxDepth)
        return self.population
            

    def getAptitudes(self):
        #evaluate Individual
        for i, individual in enumerate(self.population):
            #get sensor value from sim
            sensorValue= 5 #simulates getting closer to target for everyone
            #evaluate
            individual.evaluateTree(sensorValue)
            #get new sensor value from sim
            newSensorValue = sensorValue * random.uniform(0.0,1.0)
            individual.aptitud = 1.0/ sensorValue
            self.aptitudes[i]= individual.aptitud
        
        self.bestAptitud = max(self.aptitudes)
        self.bestParent  = self.population[self.aptitudes.index(self.bestAptitud)]
            
    
    def __cross(self, A:Tree, B:Tree):
        #copies of A and B
        A2 = A.copyTree()
        B2 = B.copyTree()

        node1 = A2.getRandomNode()
        node2 = B2.getRandomNode()

        p1 = node1.parent
        p2 = node2.parent
        index1 = 0
        index2 = 0
        if p1 != None:
            # print(node1.info, node2.info)
            for i, child in enumerate(p1.children):
                # print(child, node1)
                if child == node1: 
                    index1 = i
        if p2 != None:
            for i, child in enumerate(p2.children):
                # print(child, node2)
                if child == node2: 
                    index2 = i
        
        # print("\n\n",p1.children[index1].info, node1.info)
        # print("",p2.children[index2], node2)
        #Exchange nodes
        #node1 is root node and node2 is root node
        if p1 == None and p2 == None:
            A2.root = node2
            B2.root = node1
        #node1 is root node node2 is not root
        elif p1 == None and p2 != None:
            A2.root = node2
            p2.children[index2] = node1
            node1.parent = p2
        #node2 is root node node1 is not root
        elif p1 != None and p2 == None:
            B2.root = node1
            p1.children[index1] = node2
            node2.parent=p1
        #node1 and node2 are not root nodes
        else: 
            p1.children[index1] = node2
            node2.parent=p1
            p2.children[index2] = node1
            node1.parent = p2
        # print("\n\n",p1.children[index1], node1)
        # print("",p2.children[index2], node2)

        return A2, B2

    def parentSelection(self,m, aptitud, sel):
        """m: size of population
            aptitud: parent's list of aptitud
            sel: type of selection, tornament"""
        ParentIndexes = [None] * m
        for i in range(m):
            ParentIndexes[i]= self.selection(aptitud, sel)
        return ParentIndexes

    def selection (self,aptitud, sel):
        if sel == "torneo":
            ind = self.tournament(aptitud, 2)
        else:
            ind = self.roulette(aptitud)
        return ind


    # Seleccion por torneo.
    # Devuelve el indice del mejor individuo de t seleccionados aleatoriamente.
    def tournament(self,aptitud, t):
        # Se eligen t individuos de forma aleatoria
        sel = random.sample(range(len(aptitud)), t)
        
        # Se obtienen las aptitudes de los individuos seleccionados
        aptitudsel = list(aptitud[i] for i in sel)
        
        #Se encuentra al individuo con mejor aptitud
        win = aptitudsel.index(max(aptitudsel))

        return sel[win]


    # Seleccion por ruleta.
    # Devuelve el indice del individuo que gano en la ruleta.
    def roulette (self, aptitud):
        phi = sum(aptitud)
        rho = random.random()
        suma = 0
        while suma < rho:
            i = random.choice(range(len(aptitud)))
            suma = suma + aptitud[i] / phi
        return i

    def crossTest(self):
        return self.__cross(self.population[0],self.population[1])

    def showPopulation(self):
        for i,tree in enumerate(self.population):
            print("arbol ", i,": ")
            tree.showTree()
            print("\n\n")
        

