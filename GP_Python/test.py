from random import random
import random
from gp import GeneticProgram
from gpTree import Tree


if __name__ == "__main__":
    # t1 = Tree()
    # t1.createTreeFull(5)
    # print("[ Full method tree ]: ")
    # t1.showTree(spaces=2)
    # sensorValue = 5.0
    # robotAction = t1.evaluateTree(sensorValue)

    # print("\n\nResultado evaluación","\n\tAccción: ", robotAction)
    # print("\n\n")
    
    # print("\n")
    # node = t1.getRandomNode()
    # tt = Tree()
    # tt.root = node
    # print("\n Node: \n")
    # tt.showTree()
    # print("\n")


    # print(nodeArray)

    gp = GeneticProgram(2,"full")
    gp.show_population()
    t1,t2 = gp.cross_test()

    print("árboles con cruza")
    t1.showTree()
    t2.showTree()

