""" 
Los raiz del nodo se guardan en una lista 
junto con la instruccion que representara 

Las terminales seran los sensores junto con la lista de 
funciones: MF, TL, TR
Todas las terminales deberian ser una función
Para el primer experimento solamente se usara un sensor
"""


"""
Move forward, el robot se mueve hacia delante
toma la lista lecturas de sensores s como entrada
regresa el valor del sensor
"""
def MF(self,s):
    print("Move forward")

"""
Move forward 1, 2 y 3, el robot se mueve hacia delante con 
con una velodcidad establecida
toma la lista lecturas de sensores s como entrada
regresa un valor para avanzar, solamente en el la ultima condicion 
avanzar
"""
def MF1(self,s):
    print("Move forward 1")
    return 1

def MF2(self,s):
    print("Move forward 2")
    return 2

def MF3(self,s):
    print("Move forward 3")
    return 3

"""
Turn left, el robot gira a la izquierda 30°
toma la lista lecturas de sensores s como entrada
regresa el valor del sensor
"""
def TL(self,s):
    print("Turn left")

"""
Turn right, el robot gira a la derecha 30°
toma la lista lecturas de sensores s como entrada
regresa el valor del sensor
"""
def TR(self,s):
    print("Turn right")

"""
If bump, detecta si el robot esta esta chocando contra algo
Requiere de dos argumentos, si esta chocando se evalua el primero
si no, se evalua el segundo
"""
def IFBMP(arg1, arg2):
    pass

"""
If stuck, detecta si el robot esta atascado
Requiere de dos argumentos, si esta atascado se evalua el primero
si no, se evalua el segundo
""" 
def IFSTK(arg1, arg2):
    pass

"""
If less than or equal, condicion A <= B.
Requiere de cuatro argumentos. Hace la
comparacion entre los primeros dos argumentos. Si es 
cierta, se ejecuta el tercer argumento. Si no se ejecuta el cuarto
argumento
"""
def IFLTE(arg1, arg2, arg3, arg4):
    return arg3 if arg1 <= arg2 else arg4

"""
Toma como entrada dos argumentos, los evalua y regresa el segundo
"""
def PROGN2(arg1, arg2):
    return arg2

"""
Entrada: un arbol a y una lista de sensores s
Salida: indentificador para las funciones MF1, MF2 o MF3
"""

class Nodo:
    __1m = 1.0
    __2m = 2.0
    __5m = 5.0
    def __init__(self, hijos, dato):
        #self.padre = padre 
        self.hijos = hijos
        self.dato = dato
    
import random     

class Arbol(Nodo):
    #lista de terminales para el primer experimento
    listaTerminales = (MF1, MF2, MF3)
    listaFuciones = (IFBMP, IFSTK, IFLTE, PROGN2)
    def __init__(self, raiz=None):
        self.raiz = None
        if raiz : 
            self.raiz = raiz


    #elige todas las terminales?
    def elegirElemento(self, lista):
        return random.choice(lista)

    def crearArbolCompleto(self, profMax): 
        if profMax == 0:
            #ter <- terminales
            ter = self.elegirElemento(self.listaTerminales)
            # nodo raiz
            return Nodo(None,ter)
            
        else:
            fun = self.elegirElemento(self.listaFuciones)
            hijos= [self.crearArbolCompleto(profMax-1),self.crearArbolCompleto(profMax-1)]
            return Nodo(hijos, fun)

                    

    def crearArbolAcotado(self, profMax): 
        choice = random.randint(0, 1)
        if profMax == 0 or choice == 1:
            #ter <- terminales
            ter = self.elegirElemento(self.listaTerminales)
            # nodo raiz
            return Nodo(None,ter)
        else:
            fun = self.elegirElemento(self.listaFuciones)
            hijos= [self.crearArbolCompleto(profMax-1),self.crearArbolCompleto(profMax-1)]
            return Nodo(hijos, fun)

    def __imprimirPostorden(self, arbol, nivel = 0):
        if arbol != None: #si nodo existe
            
            if arbol.hijos!=None: 
                for i in range (len(arbol.hijos)):
                    imprimirPostorden(arbol.hijos[i], nivel+1)
            print("\t"*nivel, nivel, arbol.dato)

    def imprimirPostorden(self):
        self.__imprimirPostorden(self.raiz)
    
    def __interpretar(self,nodo):
        if self.raiz.hijos == None: #hoja
            print (self.raiz.dato)
        else:
            print (self.raiz.dato)
    def interpretar(self):
        self.__interpretar(self.raiz)
        
        


def imprimirPostorden(arbol, nivel = 0):
    if arbol != None: #si nodo existe
        if arbol.hijos!=None: 
            for i in range (len(arbol.hijos)):
                imprimirPostorden(arbol.hijos[i], nivel+1)
        print("\t"*nivel, nivel, arbol.dato)


def imprimirPreorden(arbol, nivel = 0):
    if arbol != None: #si nodo existe
        print("\t"*nivel, nivel, arbol.dato)
        if arbol.hijos!=None: 
            for i in range (len(arbol.hijos)):
                imprimirPostorden(arbol.hijos[i], nivel+1)
        
        
        