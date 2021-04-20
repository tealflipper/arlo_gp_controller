from array import array
from ruleSet import RuleSet
from rule import Rule
from gpNode import Node
import random
import yaml


class Tree:
    rules={}
    symTable={}
    initialSymb = "S"
    root = None
    depth = 0
    def __init__(self):
        self.depth=0 #TODO: update value when creating tree
        self.initialSymb="S"
        #Lista de simbolos de la regla
        S = RuleSet("S")
        S.addNonTerminalRule(Rule("SiOtro", ("ER", "S", "S") ) )
        S.addTerminalRule(Rule("Avanzar1", ("Avanzar1")))
        S.addTerminalRule(Rule("Avanzar2", ("Avanzar2")))
        S.addTerminalRule(Rule("Avanzar3", ("Avanzar3")))
        self.rules["S"]= S

        #reglas de expresion relacional
        ER = RuleSet("ER")
        ER.addNonTerminalRule(Rule("<=", ("E","E")))
        ER.addNonTerminalRule(Rule("==", ("E","E")))
        self.rules["ER"] = ER

        #Reglas para expresiones
        E = RuleSet("E")
        E.addTerminalRule(Rule("d1", ("d1")))
        E.addTerminalRule(Rule("d2", ("d2")))
        E.addTerminalRule(Rule("d3", ("d3")))
        E.addTerminalRule(Rule("SensorFrente", ("SensorFrente")))
        self.rules["E"]=E

        self.symTable["d1"] = 1.0
        self.symTable["d2"] = 5.0
        self.symTable["d3"] = 25.0
        self.symTable["Avanzar1"] = 1
        self.symTable["Avanzar2"] = 2
        self.symTable["Avanzar3"] = 3

        # Esta línea se debe agregar cuando el simulador quiera evaluar el programa
        # symTable["SensorFrente"] = valor de entrada del programa;    
    
    def __createTree(self,maxDepth=None, symbol='', bias=0.5, parent=None) -> Node:
        node = None
        rset = self.rules[symbol]
        cutTree = self.__flip(bias)
        if maxDepth == None: return None

        if ((maxDepth <= 0 and rset.numTerminals() > 0) or
        (cutTree and rset.numTerminals() > 0) or
        rset.onlyTerminals()):

            #get random terminal rule from symbols
            r= rset.Terminals[ self.__randInt(rset.numTerminals())]
            node = Node(info=r.ruleName,arity=0,parent=parent)
        else: 
            # maxDepth != 0 or only has NT, For sure has NT and flip is false
            # choose random NT rule from symbol
            r= rset.NonTerminals[ self.__randInt(rset.numNonTerminals())]
            node = Node(r.ruleName,r.numSymbols(),parent=parent)

            for i in range(r.numSymbols()):
                node.setChild(i, self.__createTree(maxDepth-1, r.members[i], bias, parent=node))

        return node

    def __flip(self, bias) -> bool:
        rnd = random.uniform(0.0,1.0)
        if rnd > bias: return True
        else: return False

    def __randInt(self, limit) -> int:
        return random.randint(0,limit-1)

    def __evaluateTree(self, root) -> float:
        if root.isTerminal(): 
            return self.symTable[root.info]
        else:
            if root.info == "SiOtro":
                testValue = self.__evaluateTree(root.getChild(0))
                branchVal = None
                if testValue == 1.0:
                    branchVal = self.__evaluateTree(root.getChild(1))
                else: 
                    branchVal = self.__evaluateTree(root.getChild(2))
                return branchVal

            else:
                leftVal = self.__evaluateTree(root.getChild(0))
                rightVal = self.__evaluateTree(root.getChild(1))
                return self.__apply(root.info, leftVal, rightVal)

    def __apply(self, op, v1,v2) -> float:
        if op == "<="   : return 1.0 if v1 <= v2 else 0.0
        elif op == "<"    : return 1.0 if v1 < v2 else 0.0
        elif op == "=="   : return 1.0 if v1 == v2 else 0.0
        elif op == "+"    : return v1 + v2
        elif op == "*"    : return v1*v2
        else: 
            print("[Apply] Unknown Operator")
            return 0.0

    def __showTree(self,root, level, spaces=None):
        if root != None: 
            if root.isFunction(): 
                print("")
                if spaces == None:print("\t"*level,end = '')
                else: print(" "*(int(spaces)*level),end = '')
                print("( ",end = '')
            
            print(" ",root.info, end=' ')
            
            for i in range(root.getArity()):
                self.__showTree(root.getChild(i), level+1)
            
            if root.isFunction(): print(" )",end = '')

    def createTreeFull(self, maxDepth) -> Node:  
        self.root = self.__createTree(maxDepth, self.initialSymb, 1.0)
        self.depth = maxDepth
        return self.root

    def createTreeGrow(self, maxDepth) -> Node:
        self.root = self.__createTree(maxDepth, self.initialSymb, 0.5)
        self.depth = maxDepth
        return self.root
        
    def evaluateTree(self,sensorValue) -> float:
        self.symTable["SensorFrente"] = sensorValue
        print("\n\n")
        self.showSymTable()
        return self.__evaluateTree(self.root)

    def showTree(self, spaces=None):
        self.__showTree(self.root, 0, spaces)
        
    def showSymTable(self):
        print(yaml.dump({"Symbol Table":self.symTable}, indent = 2))

    def __mutate(self,root,pm):
        """ Recorre todo el arbol y en cada nodo si el numero aleatorio es 
            menor o igual a pm, probabilidad de mutación"""
        if root != None and random.random() <= pm:
            # print(root.info, self.rules["S"].Terminals[0].ruleName)
            lvl = random.randint(1,8)
            for key in self.rules:
                rset = self.rules[key]
                if root.info in rset.getRuleset():
                    #make new branch
                    cutTree = self.__flip(0.5)
                    if (cutTree and rset.numTerminals() > 0 or
                        rset.onlyTerminals()):
                        r = rset.Terminals[ self.__randInt(rset.numTerminals())]
                        root.info = r.ruleName
                        root.children = []
                        print (key,root.info)
                    else: 
                        r = rset.NonTerminals[ self.__randInt(rset.numNonTerminals())]
                        root.info = r.ruleName
                        root.arity = r.numSymbols()
                        root.children = [None]*root.arity
                        for i in range(r.numSymbols()):
                            root.setChild(i, self.__createTree(lvl, r.members[i], 0.5))
                        print (key,root.info)
                        return root
                else: 
                    for child in root.children:
                        self.__mutate(child,pm)

    def __copyTree(self,root):
        new_tree = Node(root.info,root.arity,root.parent,root.type)
        for i, child in enumerate(root.children):
            new_tree.children[i] = child
        for i in range(len(root.children)):
            new_tree.children[i]=self.__copyTree(root.children[i])
        return new_tree

    def copyTree(self):
        new_tree = Tree()
        new_tree.root = self.__copyTree(self.root)
        new_tree.depth = self.depth
        return new_tree

    def __getNodeArray(self, root,p, array):
        if root != None:
            # print(" ",root.info)
            array.append(root)
            for child in root.children:
                self.__getNodeArray(child, p*2, array)

            

    def getNodeArray(self):
        array = []
        self.__getNodeArray(self.root,0.01,array)
        return array

    def choseNode(self):
        nodeArray = self.getNodeArray()
        beg = (len(nodeArray)//10)
        print(beg)
        place = random.randint(1,len(nodeArray)-1)
        print(place)
        return nodeArray[place]

    
    def mutate(self, pm):
        # print(self.root.info, self.rules["S"].getRuleset())
        self.__mutate(self.root, pm)