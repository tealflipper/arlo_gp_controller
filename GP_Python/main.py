from gpTree import Tree


if __name__ == "__main__":
    t1 = Tree()
    t1.createTreeFull(3)
    print("[ Full method tree ]: ")
    t1.showTree(spaces=2)
    sensorValue = 5.0
    robotAction = t1.evaluateTree(sensorValue)

    print("\n\nResultado evaluación","\n\tAccción: ", robotAction)
    print("\n\n")
    

    t2 = Tree()
    t2.createTreeGrow(3)
    print("[ Grow method tree ]: ")
    t2.showTree(2)
    sensorValue = 5.0
    robotAction = t2.evaluateTree(sensorValue)

    print("\n\nResultado evaluación","\n\tAccción: ", robotAction)