from ruleSet import RuleSet
from rule import Rule
from gpNode import Node


class Tree:
    rules={}
    symTable={}
    def __init__(self):
        self.root = None
        self.depth=0
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
        ER.addNonTerminal(Rule("<=", ("E","E")))
        ER.addNonTerminal(Rule("==", ("E","E")))
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
    
    def __createTree(self,maxDepth, symbol, bias):
        node = None

        rset = self.rules[symbol]

    def __flip(self, bias):
        pass

    def __randInt(self, limit):
        pass

    def __showTree(self,root, level):
        pass

    def createTreeFull(self,maxDepth, symbol, bias):  
        pass
    def createTreeGrow(self,maxDepth, symbol, bias):
        pass
    def evaluateTree(self,sensorValue=None, root= None):
        pass
    def showTree(self):
        self.__showTree(self.root, 0)
        
    def showSymTable(self):
        pass
    def apply(self, d1,d2):
        pass