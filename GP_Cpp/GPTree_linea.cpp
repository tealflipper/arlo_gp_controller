#include "GPTree.h"
#include "RuleSet.h"
#include <iostream>
#include <random>

using namespace std;

/*********************************************************************
* Constructor del árbol donde solamente se crea la "Tabla" de regrelas
* de producción para crear el árbol. El árbol se crea invocando alguno
* de los 2 métodos, createTreeFull y createTreeGrow (ver abajo).
*********************************************************************/
GPTree::GPTree()
{
   root = nullptr;
   depth = 0; // TODO: actualizar este atributo al crear el árbol.

   // Agregar las reglas de producción de la gramática

   initialSymb = "S";

   // Conjunto de reglas para Sentencia.
   RuleSet S("S");
           // Nombre de la regla, {lista de símbolos de la regla}
   S.addNonTerminalRule(Rule("SiOtro", {"ER", "S", "S"}));
   S.addTerminalRule(Rule("Avanzar1", {"Avanzar1"}));
   S.addTerminalRule(Rule("Avanzar2", {"Avanzar2"}));
   S.addTerminalRule(Rule("Avanzar3", {"Avanzar3"}));
   rules.insert(pair<string,RuleSet>("S", S));

   // Conjunto de reglas para ExprRelacional.
   RuleSet ER("ER");
   ER.addNonTerminalRule(Rule("<=", {"E", "E"}));
   ER.addNonTerminalRule(Rule("==", {"E", "E"}));
   rules.insert(pair<string,RuleSet>("ER", ER));

   // Conjunto de reglas para Expr.
   RuleSet E("E"); // Expr
   E.addTerminalRule(Rule("d1", {"d1"}));
   E.addTerminalRule(Rule("d2", {"d2"}));
   E.addTerminalRule(Rule("d3", {"d3"}));
   E.addTerminalRule(Rule("SensorFrente", {"SensorFrente"}));
   rules.insert(pair<string,RuleSet>("E", E));

   symTable["d1"] = 1.0;
   symTable["d2"] = 5.0;
   symTable["d3"] = 10.0;
   symTable["Avanzar1"] = 1; // El simulador sabrá qué hacer con este código.
   symTable["Avanzar2"] = 2; // El simulador sabrá qué hacer con este código.
   symTable["Avanzar3"] = 3; // El simulador sabrá qué hacer con este código.

   // Esta línea se debe agregar cuando el simulador quiera evaluar el programa
   //symTable["SensorFrente"] = valor de entrada del programa;

   //cerr << "\nTerminó el constructor.\n";
}
/*********************************************************************
* TODO: liberar la memoria de los nodos al recorrer el árbol recursivamente.
*********************************************************************/
GPTree::~GPTree() {
   //cout << "\nDestruyendo el árbol.\n\n";
   destroyTree(root);
}

/*
* Este es el método general para crea árboles:
* Si bias = 1, entonces se comportará con el método FULL, and
* Si bias < 1, se comporta como el métod GROW.
* Entre más grande sea el sesgo, es más probable que el árbol crezca hasta
* alcanzar su profunidad máxima.
* Podríamos pensar al sesgo como el tamaño esperardo del árbol
* (1, crece al máximo, 0 crece al mínimo).
*/
GPNode* GPTree::createTree(int maxDepth, string symbol, double bias) {
   //cerr << "\ncreateTree: " << "maxDepth= " << maxDepth << ", symbol= " << symbol << endl;

   GPNode* node = nullptr;

   // Conjunto de todas las reglas del símbolo 'symbol'.
   RuleSet rset = rules.find(symbol)->second;

   bool cortar = flip(bias); // Aleatoriamente decidimos si cortamos antes el árbol.
   if (( maxDepth<=0 && rset.numTerminals()>0 ) || /* Se alcanzó prof. máx. y sí tiene terminales, OR */
       ( cortar && rset.numTerminals()>0 ) ||      /* El flip dice que hay que cortar y sí tiene terminales. */
         rset.onlyTerminals() )                    /* Ya solamente tiene terminales que poner, OR */
   {
      // Elegir aleatoriamente una regla terminal del símbolo de entrada.
      Rule r = rset.getTerminalRule( rndInt(rset.numTerminals()) );
      //cerr << "\n Se decidió CORTAR, flip= " << cortar << ", regla elegida: " << r.getRuleName() << endl;
      node = new GPNode(r.getRuleName(), 0);  // 0 hijos
   }
   else { // (maxDepth != 0 ó solo tiene NT) y seguro tiene No Terminales y flip es falso
      // Elegir aleatoriamente una regla NO terminal del símbolo de entrada.
      Rule r = rset.getNonTerminalRule(rndInt(rset.numNonTerminals()));
      //cerr << "\n Se decidió SEGUIR, " << " eligiendo la regla: " << r.getRuleName() << endl;
      //cerr << ", su número de hijos es " << r.numSymbols() << endl;
      node = new GPNode(r.getRuleName(), r.numSymbols());

      for (int i = 0; i < r.numSymbols(); ++i)
         node->setChild(i, createTree(maxDepth-1, r.getElement(i), bias));
   }

   return node;
}


/*********************************************************************
* Use createTree with bias=1.0 to implement the Full method.
*********************************************************************/
GPNode* GPTree::createTreeFull(int maxDepth)
{
   root = createTree(maxDepth, initialSymb, 1.0);
   return root;
}


/*********************************************************************
* Use createTree with bias=0.5 to implement the Grow method.
* I.e., there is a chance of 50% of cutting a branch before reaching
* the maximum depth.
*********************************************************************/
GPNode* GPTree::createTreeGrow(int maxDepth)
{
   root = createTree(maxDepth, initialSymb, 0.5);
   return root;
}

/*
 * This is the method the simulator will use to obtain the action for the robot.
 * The only parameter is the sensor value.
 * The returning value is any of these 3 values:
 * - Value 1.0 (Avanzar1)
 * - Value 2.0 (Avanzar2)
 * - Value 3.0 (Avanzar3)
 * The simulator should implement these actions in the robot.
 */
double GPTree::evaluateTree(double sensorValue)
{
   symTable["SensorFrente"] = sensorValue;

   // Show the values of the Symbol Table (constants and variables).
   cout << "Tabla de símbolos\n";
   showSymTable();

   return evaluateTree(root); // internal method that implements the evaluation.
}

/**************************************************************************
* Main method for evaluating the current tree starting from the root and using
* the current value in the Symbol Table.
***************************************************************************/
double GPTree::evaluateTree(GPNode* root)
{
   if (root->isTerminal()) {
      // Si es terminal (constante, variable, acción robot), regresar su valor.
      return symTable[root->getInfo()];
   }
   else { // Entonces estamos en una función (Estrucutura de control, comparación, op. aritmética)
      // Si la función es "SiEntoncesOtro".
      if  (root->getInfo() == "SiOtro") {
         // Evaluamos la condición (Hijo 0)
         double testValue = evaluateTree(root->getChild(0)); // regresa 0, 1
         double branchValue;

         // Si la condición es verdadera SOLO evaluamos el hijo 1.
         if (testValue == 1.0)  //True = 1, False = 0
            branchValue = evaluateTree(root->getChild(1));  // TRUE branch
         else // En otro caso, SOLO evaluamos el hijo 2.
            branchValue = evaluateTree(root->getChild(2));  // FALSE branch

         return branchValue;
      }
      else { // Es una función binaria relacional o aritmética.
         // En esta versión, la única opción es "<=" o "==", pero se evalúan igual.
         double leftValue  = evaluateTree(root->getChild(0));
         double rightValue = evaluateTree(root->getChild(1));
         return apply(root->getInfo(), leftValue, rightValue);
      }
   }
   return 0.0;
}

/*
 * Este método evalúa tanto operaciones relacionales (<, !=, etc.) como aritméticas.
 */
double GPTree::apply(string operador, double op1, double op2) {
   if (operador == "<=") {
      return (op1 <= op2) ? 1 : 0;
   }
   if (operador == "<") {
      return (op1 < op2) ? 1 : 0;
   }
   else if (operador == "==") {
      return (op1 == op2) ? 1 : 0;
   }
   else if (operador == "!=") {
      return (op1 != op2) ? 1 : 0;
   }
   else if (operador == "+") {
      return op1 + op2;
   }
   else if (operador == "*") {
      return op1 * op2;
   }
   else {
      cerr << "Función apply: el operador '" << operador << "' NO es conocido.\n";
      return 0;
   }
}


/*********************************************************************
* Este método muestra el árbol usando una notación como la de LISP,
* es decir (FUNCIÓN  ARG1  ARG2 ... ARGN), donde ARG puede ser todo un
* subárbol de expresiones.
* Es solamente una forma de mostrar, NO quiere decir que el programa
* del árbol solamente puede ser LISP. También se podría mostrar como un
* programa en C o Python si quisiéramos.
* Por ejemplo, este árbol se mostraría así (LISP):
* (SiOtro
*        (<= SensorFrente d2 ) Avanzar1 Avanzar2 )
*
* En notación de C esto significaría:
* if (SensorFrente <= d2)
*    return Avanzar1;
* else
*    return Avanzar2;
*********************************************************************/
void GPTree::showTree()
{
   showTree(root, 0);
}

/*
 * Véase método showTree() de arriba.
 * El parámetro level solamente sirve para mostrar el contenido
 * con una indentación apropiada según el nivel del árbol.
 */
void GPTree::showTree(GPNode* root, int level)
{
   if (root != nullptr) {
      if (root->isFunction()) {
         cout << "\n";

         for (int i = 0; i < level; ++i)
            cout << "\t";
      }

      if (root->isFunction())
         cout << "(";

      cout << root->getInfo() << " ";
      for (int i = 0; i < root->getArity(); ++i)
         showTree(root->getChild(i), level+1);

      if (root->isFunction())
         cout << ") ";
   }
}

bool GPTree::flip(double bias) {
   random_device rd;  //Will be used to obtain a seed for the random number engine
   mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
   uniform_real_distribution<> dis(0.0, 1.0);

   double rnd = dis(gen);
   if (rnd > bias)
      return true;
   else
      return false;
}

int GPTree::rndInt(int limit) {
   random_device rd;  //Will be used to obtain a seed for the random number engine
   mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
   uniform_int_distribution<> dis(0, limit-1);

   return dis(gen);
}

void GPTree::showSymTable() {
   for (auto sym: symTable)
      cout << sym.first << ": " << sym.second << "\n";
}

/*
 * Recorrer el árbol en POST orden (al final la raíz) para liberar la memoria.
 */
void GPTree::destroyTree(GPNode* root) {
   if (root != nullptr) {
      //Liberar primero los hijos (si los tiene).
      for (int i = 0; i < root->getArity(); ++i)
         destroyTree(root->getChild(i));

      //Liberar al padre
      delete root;
   }
}
