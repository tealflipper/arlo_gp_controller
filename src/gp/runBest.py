#!/usr/bin/env python3
from __future__ import annotations
import re
from gpTree import Tree
import rospy
from gp import GeneticProgram

from arlo_gp_controller.srv import EvaluateTree, EvaluateTreeResponse
from arlo_nn_controller.srv import EvaluateDriver

#used to save object to file
import pickle

if __name__ == "__main__":
    rospy.init_node('gp', anonymous=True)

    print("Mejor Individuo \n --------------------------------------\n")
    gp = None
    def handleEvaluateTree(req):
        # print("evaluate tree:", req )
        individual = None
        evalBest = True if req.treeIndex == -1 else False
        if evalBest : 
            individual =  gp.bestParent
        else :
            individual = gp.population[req.treeIndex]
        
        actuatorValues = individual.evaluateTree(req.sensorValues)
        #print("actuator values:", actuatorValues)
        return EvaluateTreeResponse(actuatorValues)

    server = rospy.Service('evaluate_tree',EvaluateTree, handler=handleEvaluateTree)
    rospy.wait_for_service('evaluate_driver')
    evaluateDriverClient = rospy.ServiceProxy('evaluate_driver', EvaluateDriver)

    with open ('gp.dat', 'rb') as gpFile:
        gp = pickle.load(gpFile)
        gp.besParent = Tree()
        print('GP loaded from gp.dat\n')
        gp.population[0].showSymTable()
        
    
    print("Best individual")
    print("Aptitud:",gp.bestAptitud)
    gp.bestParent.showTree()
    evaluateDriverClient(60,-1)
    # save gp to file
    #keep active until kill signal is sentpop
    # rospy.spin()
