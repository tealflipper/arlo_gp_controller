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

    print("Programa Genetico \n --------------------------------------\n")
    popSize = int(input("population size: "))
    generations = int(input("number of generations: "))
    treeDepth   = int(input("max tree depth: "))
    mutationProbability = float(input("mutation probability: "))
    gp = GeneticProgram(popSize, generations, treeDepth, 'full', mutationProbability)
    
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

    gp.setInitialPopulation()
    print("Genetic Program Start")
    for generation in range(gp.maxGen):
        print("generation:", generation)
        for index in range(gp.popSize):
            print("\tIndividual: ",index)
            #maxtime, treeIndex
            driverResponse = evaluateDriverClient(60,index)
            gp.setAptitude(index,driverResponse.dist2go)

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
    print("Best individual")
    print("Aptitud:",gp.bestEver.aptitud)
    gp.bestEver.showTree()
    evaluateDriverClient(60,-1)
    # save gp to file
    with open ('gp.dat', 'wb') as gpFile:
        pickle.dump(gp, gpFile )
        print('GP saved to gp.dat')
    #keep active until kill signal is sentpop
    # rospy.spin()
