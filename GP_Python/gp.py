from array import array
from gpTree import Tree
from gpNode import Node
import random

class GeneticProgram:
    population = []
    def __init__(self, size, type) -> None:
        
        for i in range(size):
            self.population.append(Tree())
            randsize = 3 #TODO: change to random int
            if type == "full":
                self.population[i].createTreeFull(randsize)
            else:
                self.population[i].createTreeGrow(randsize)
                
    #TODO: change copy node function to change parent in node copy
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
        
        # print(node1.info, node2.info)
        for i, child in enumerate(p1.children):
            # print(child, node1)
            if child == node1: 
                index1 = i
        
        for i, child in enumerate(p2.children):
            # print(child, node2)
            if child == node2: 
                index2 = i
        
        # print("\n\n",p1.children[index1].info, node1.info)
        # print("",p2.children[index2], node2)
        #Exchange nodes
        p1.children[index1] = node2
        node2.parent=p1
        p2.children[index2] = node1
        node1.parent = p2
        # print("\n\n",p1.children[index1], node1)
        # print("",p2.children[index2], node2)

        return A2, B2


        
        
        return A2, B2

    def crossTest(self):
        return self.__cross(self.population[0],self.population[1])

    def showPopulation(self):
        for i,tree in enumerate(self.population):
            print("arbol ", i,": ")
            tree.showTree()
            print("\n\n")
    

