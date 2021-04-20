from gpTree import Tree


if __name__ == "__main__":
    t1 = Tree()
    t1.createTreeFull(10)
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
    t1.showTree()
    print("\n")
    t1.mutate(0.9)
    t1.showTree()
    print("\n")
    t1_copy = t1.copyTree()
    t1_copy.showTree()

    node = t1.chooseNode()

    print("\n Node: \n")
    tt = Tree ()
    tt.root = node
    tt.showTree()
    print("\n")
    print(node.info)
