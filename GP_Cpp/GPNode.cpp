/*
 * GPNode.cpp
 *
 *  Created on: 8 feb 2021
 *      Author: antonio
 */

#include "GPNode.h"

GPNode::GPNode(string info, int arity, NodeType type) : GPNode(info, arity)
{
   this->type =type;
}

GPNode::GPNode(string info, int arity) {
   this->info = info;
   this->arity = arity;
   this->type = (arity == 0)? TERMINAL : FUNCTION;
   children.resize(this->arity, nullptr);
   value = 0.0;
}

GPNode::~GPNode() {}

int GPNode::getArity() {
   return children.size();
}

void GPNode::setChild(int i, GPNode* child) {
   children[i] = child;
}

GPNode* GPNode::getChild(int i) {
   if (arity == 0)
      return nullptr;
   else
      return children[i];
}

string GPNode::getInfo() {
   return info;
}

bool GPNode::isTerminal() {
   return (arity == 0);
}

bool GPNode::isFunction() {
   return (arity > 0);
}




