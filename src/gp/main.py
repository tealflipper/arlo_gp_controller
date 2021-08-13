#!/usr/bin/env python3
from __future__ import annotations
import rospy
from gp import GeneticProgram

from arlo_gp_controller.srv import EvaluateTree, EvaluateTreeResponse
from arlo_nn_controller.srv import EvaluateDriver


if __name__ == "__main__":
    rospy.init_node('gp', anonymous=True)

    print("Programa Genetico \n --------------------------------------\n")
    gp = GeneticProgram(4, 1, 5, 'full', 0.02)
    
    def handleEvaluateTree(req):
        # print("evaluate tree:", req )
        individual = gp.population[req.treeIndex]
        sensorValue = req.sensorValues[15]
        actuatorValues = individual.evaluateTree(sensorValue)
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
            driverResponse = evaluateDriverClient(20,index)
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
    print("Aptitud:",gp.bestAptitud)
    gp.bestParent.showTree()
    #keep active until kill signal is sent
    # rospy.spin()
