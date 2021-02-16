#include <iostream>
#include "GPTree.h"

int main(int argc, char* argv[])
{
   // Ejemplo1: un árbol creado con el método FULL con profunidad 3.
   GPTree tree1;
   tree1.createTreeFull(3);

   cerr << "\n****** Arbol creado con el método Full:\n";
   tree1.showTree();


   // Ejemplo2: un árbol creado con el método GROW con profundidad máxima de 3.
   GPTree tree2;
   tree2.createTreeGrow(3);

   cerr << "\n\n****** Arbol creado con el método Grow:\n";
   tree2.showTree();
   cout << "\n\n";

   // Evaluación del árbol suponiendo que el simulador le pasa
   // el valor actual del sensor igual a 5.0.
   double sensorValue = 5.0;
   double robotAction = tree2.evaluateTree(sensorValue);

   cout << "\n\nResultado de la evaluación";
   cout << "\n\tAcción: " << robotAction << "\n\n";

   return 0;
}
