#ifndef GPNODE_H
#define GPNODE_H

#include <string>
#include <vector>
#include <utility>

using namespace std;

enum NodeType {FUNCTION, TERMINAL, LOGIC, VARIABLE, CONSTANT, ACTION};

class GPNode {
public:
   GPNode(string info, int arity, NodeType type);
   GPNode(string info, int arity);
   ~GPNode();

   int getArity();
   void setChild(int i, GPNode* child);
   GPNode* getChild(int i);
   string getInfo();
   bool isTerminal(); // Equivalente to arity = 0 or isLeaf
   bool isFunction();

   //double getValue();
   //void setValue(double);
   //bool isVariable();
   //bool isConstant();
   //bool isApplication();
   //NodeType getType();

private:
   int arity;      /* Number of children */
   NodeType type;  /* Type of node (function or terminal)*/
   string info;    /* Symbol stored in the node */
   vector<GPNode*> children; /* Reference for this node's children */

   /* Si el nodo es terminal y tiene variable o constante. */
   double value; /* variable's value */

};

#endif
