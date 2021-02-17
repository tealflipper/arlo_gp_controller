class Rule:
    def __init__(self, name, elements):
        self.ruleName = name
        self.members = elements
    
    def numSymbols(self):
        return len(self.members)
    
    def getElement(self,i):
        return self.members[i]