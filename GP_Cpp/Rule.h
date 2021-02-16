#ifndef RULE_H
#define RULE_H

#include <string>
#include <vector>

using namespace std;

class Rule {
public:
   Rule(string name, vector<string> elements);
   ~Rule();

   int numSymbols();
   string getRuleName();
   string getElement(int i);

private:
   string ruleName;
   vector<string> members;
};

#endif
