from rule import Rule

class RuleSet:
    def __init__(self,symbol):
        self.symbol = symbol
        self.Terminals = []
        self.NonTerminals = []

    def addTerminalRule(self, rule):
        self.Terminals.append(rule)

    def addNonTerminalRule(self, rule):
        self.NonTerminals.append(rule)
    
    def numTerminals(self):
        return len(self.Terminals)
    
    def numNonTerminals(self):
        return len(self.NonTerminals)

    def onlyTerminals(self):
        return (self.numTerminals()>0 and self.numNonTerminals()==0)

    def onlyNonTerminals(self):
        return (self.numNonTerminals()>0 and self.numTerminals()==0)

    