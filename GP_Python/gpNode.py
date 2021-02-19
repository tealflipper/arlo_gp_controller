from __future__ import annotations
from enum import Enum

#Node Type
class NType(Enum):
    FUNCTION    = 1
    TERMINAL    = 2
    LOGIC       = 3
    VARIABLE    = 4
    CONSTANT    = 5
    ACTION      = 6

class Node:
    def __init__(self, info, arity, type=None):
        self.info = info
        self.arity = arity
        if type != None: 
            self.type = type
        else: 
            self.type = NType.TERMINAL if arity == 0 else NType.FUNCTION
        
        self.children = [None]*arity
        self.value = 0.0

    def getArity(self) -> int:
        return len(self.children)

    def setChild(self, i, child):
        self.children[i]=child

    def getChild(self, i) -> Node:
        if self.arity == 0:
            return None
        else:
            return self.children[i]

    def isTerminal(self)->bool:
        return (self.arity == 0)

    def isFunction(self)->bool:
        return (self.arity > 0) 

