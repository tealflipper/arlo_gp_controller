#include "RuleSet.h"


/*********************************************************************
* Comment
*********************************************************************/
RuleSet::RuleSet(string symbol)
{
   this->symbol = symbol;
}

/*********************************************************************
* Comment
*********************************************************************/
RuleSet::~RuleSet() {}

string RuleSet::getSymbol() {
   return symbol;
}

/*********************************************************************
* Comment
*********************************************************************/
void RuleSet::addTerminalRule(Rule r)
{
   Terminals.push_back(r);
}

void RuleSet::addNonTerminalRule(Rule r)
{
   NonTerminals.push_back(r);
}

/*********************************************************************
* Comment
*********************************************************************/
Rule RuleSet::getTerminalRule(int i)
{
   return Terminals.at(i);
}

Rule RuleSet::getNonTerminalRule(int i)
{
   return NonTerminals.at(i);
}

/*********************************************************************
* Comment
*********************************************************************/
int RuleSet::numTerminals()
{
   return Terminals.size();
}
/*********************************************************************
* Comment
*********************************************************************/
int RuleSet::numNonTerminals()
{
   return NonTerminals.size();
}

/*********************************************************************
* Comment
*********************************************************************/
bool RuleSet::onlyTerminals()
{
   return (Terminals.size() > 0 && NonTerminals.size() == 0);
}

/*********************************************************************
* Comment
*********************************************************************/
bool RuleSet::onlyNonTerminals()
{
   return (NonTerminals.size() > 0 && Terminals.size() == 0);
}
