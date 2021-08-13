#!/usr/bin/env python3
from __future__ import annotations
import rospy
from gp import GeneticProgram

from arlo_gp_controller.srv import EvaluateTree, EvaluateTreeResponse
from arlo_nn_controller.srv import EvaluateDriver


if __name__ == "__main__":
    rospy.init_node('gp', anonymous=True)

    print("Programa Genetico \n --------------------------------------\n")
    gp = GeneticProgram(4, 3, 5, 'full', 0.2)
    
    def handleEvaluateTree(req):
        print("evaluate tree:", req )
        individual = gp.population[req.treeIndex]
        sensorValue = req.sensorValues[15]
        actuatorValues = individual.evaluateTree(sensorValue)
        print(actuatorValues)
        return EvaluateTreeResponse(actuatorValues)

    server = rospy.Service('evaluate_tree',EvaluateTree, handler=handleEvaluateTree)
    rospy.wait_for_service('evaluate_driver')
    evaluateDriverClient = rospy.ServiceProxy('evaluate_driver', EvaluateDriver)

    gp.setInitialPopulation()

    for i in range(gp.maxGen):
        
        for index in range(gp.popSize):
            #maxtime, treeIndex
            driverResponse = evaluateDriverClient(5,index)
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

    #gp.showPopulation()
    #keep active until kill signal is sent
    rospy.spin()
