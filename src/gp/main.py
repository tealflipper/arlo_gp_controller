#!/usr/bin/env python3

import rospy
from gp import GeneticProgram, handleEvaluateTree

from arlo_gp_controller.srv import ActuatorValuesService, ActuatorValuesServiceResponse

if __name__ == "__main__":
    rospy.init_node('gp', anonymous=True)

    server = rospy.Service('actuator_values',ActuatorValuesService, handler=handleEvaluateTree)
    
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
    gp.setInitialPopulation()

    for i in range(gp.maxGen):
        
        for index in range(gp.popSize):
            gp.setAptitude(index)
            
        gp.setBestAptitud()
        gp.setBestParent()
        #select parents
        gp.setParents('torneo')
        #cross
        #print(parents)
        gp.cross()
        #     #mutate
        gp.mutatePopulation()
        # print('pop', self.population)

    #gp.showPopulation()
