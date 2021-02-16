#ifndef GPTREE_H
#define GPTREE_H

#include "GPNode.h"
#include "RuleSet.h"
#include <string>
#include <vector>
#include <map>
#include <utility>

using namespace std;

class GPTree {
public:
   GPTree();
   ~GPTree();

   GPNode* createTreeFull(int maxDepth);
   GPNode* createTreeGrow(int maxDepth);
   void destroyTree(GPNode* root);
   double evaluateTree(double sensorValue);
   double evaluateTree(GPNode* root);
   void showTree();
   void showTree(GPNode* root, int level);
   void showSymTable();
   double apply(string, double, double);

private:
   GPNode* createTree(int maxDepth, string symbol, double bias);
   bool flip(double bias);
   int rndInt(int limit);

   map<string, RuleSet> rules; // TODO: debería ser un parámetro de entrada?

   string initialSymb;

   map<string, double> symTable;

   GPNode* root;  /* Tree's root */
   int depth;
};

#endif
