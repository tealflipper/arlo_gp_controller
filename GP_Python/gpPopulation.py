from gpTree import Tree
import random


class Population:

    def __init__(self, size, type) -> None:
        self.population = []
        for i in range(size):
            self.population.append(Tree())
            randsize = 5 #TODO: change to random int
            if type == "full":
                self.population[i].createTreeFull(randsize)
            else:
                self.population[i].createTreeGrow(randsize)
                
    def cross(self, A, B, bias):
        A2 = A.copyTree()
        B2 = B.copyTree()
        A2_cross_node = A2.chooseNode(bias)
        B2_cross_node = B2.chooseNode(bias)
        temp_node = A2_cross_node
        A2_cross_node = B2_cross_node
        B2_cross_node = temp_node

