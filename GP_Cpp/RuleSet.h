#ifndef RULESET_H
#define RULESET_H

#include "Rule.h"

class RuleSet {
public:
   RuleSet(string symbol);
   ~RuleSet();
   string getSymbol();
   void addTerminalRule(Rule r);
   void addNonTerminalRule(Rule r);
   Rule getTerminalRule(int i);
   Rule getNonTerminalRule(int i);
   int numTerminals();
   int numNonTerminals();
   bool onlyTerminals();
   bool onlyNonTerminals();

private:
   string symbol;
   vector<Rule> Terminals;
   vector<Rule> NonTerminals;
};

#endif
