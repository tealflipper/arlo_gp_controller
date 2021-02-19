from ruleSet import RuleSet
from rule import Rule
from gpNode import Node
import random
import yaml
rules = {}

S = RuleSet("S")
S.addNonTerminalRule(Rule("SiOtro", ("ER", "S", "S") ) )
S.addTerminalRule(Rule("Avanzar1", ("Avanzar1")))
S.addTerminalRule(Rule("Avanzar2", ("Avanzar2")))
S.addTerminalRule(Rule("Avanzar3", ("Avanzar3")))
rules["S"]= S

rset = rules["S"].symbol
symbol = "S"

print(rset)
print(random.randint(0,5))
maxDepth = 1
node = None
rset = rules[symbol]
cutTree =False
if ((maxDepth <= 0 and rset.numTerminals) or
    (cutTree and rset.onlyTerminals()) or
    rset.onlyTerminals()):
    #get random terminal rule from symbols
    r= rset.Terminals[1]
    node = Node(r.ruleName,0)
else: 
    # maxDepth != 0 or only has NT, For sure has NT and flip is false
    # choose random NT rule from symbol
    r= rset.NonTerminals[0]
    node = Node(r.ruleName,r.numSymbols())

a={'A':{'speed':70,
        'color':2},
        'B':{'speed':60,
        'color':3}}
print(yaml.dump(a, indent = 2))