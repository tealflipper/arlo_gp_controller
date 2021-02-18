from ruleSet import RuleSet
from rule import Rule

rules = {}

S = RuleSet("S")
S.addNonTerminalRule(Rule("SiOtro", ("ER", "S", "S") ) )
S.addTerminalRule(Rule("Avanzar1", ("Avanzar1")))
S.addTerminalRule(Rule("Avanzar2", ("Avanzar2")))
S.addTerminalRule(Rule("Avanzar3", ("Avanzar3")))
rules["S"]= S

rset = rules["S"].symbol


print(rset)