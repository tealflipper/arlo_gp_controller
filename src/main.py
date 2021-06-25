#!/usr/bin/env python3

import rospy
from gp import GeneticProgram


if __name__ == "__main__":

    rospy.init_node('gp', anonymous=True)

    # t1 = Tree()
    # t1.createTreeFull(5)
    # print("[ Full method tree ]: ")
    # t1.showTree(spaces=2)
    # sensorValue = 5.0
    # robotAction = t1.evaluateTree(sensorValue)

    # print("\n\nResultado evaluación","\n\tAccción: ", robotAction)
    # print("\n\n")
    

    # t2 = Tree()
    # t2.createTreeGrow(3)
    # print("[ Grow method tree ]: ")
    # t2.showTree(2)
    # sensorValue = 5.0
    # robotAction = t2.evaluateTree(sensorValue)

    # print("\n\nResultado evaluación","\n\tAccción: ", robotAction)
    # t1.showTree()
    # print("\n")
    # t1.mutate(0.9)
    # t1.showTree()
    # print("\n")
    # t1_copy = t1.copyTree()
    # t1_copy.showTree()

    # node = t1_copy.getRandomNode()

    # print("\n Node: \n")
    # tt = Tree ()
    # tt.root = node
    # tt.showTree()
    # print("\n")
    # print(node.info)
    print("Programa Genetico \n --------------------------------------\n")
    gp = GeneticProgram(4, 3, 5, 'full', 0.2)
    gp.showPopulation()
