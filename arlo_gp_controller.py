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
def interpretar(a, s):
    pass
class Nodo:
    __1m = 1.0
    __2m = 2.0
    __5m = 5.0
    def __init__(self, padre, hijos, dato):
        self.padre = padre 
        self.hijos = hijos
        self.dato = dato
    
import random     

class Arbol:
    #lista de terminales para el primer experimento
    listaTerminales = ("MF1", "MF2", "MF3")
    def __init__(self):
        hijos = []
        dato="null"
        return Nodo(hijos, NULL, dato)
    #elige todas las terminales?
    def elegirElemento(self):
        return random.choice(self.listaTerminales)

    def crearArbolCompleto(self, profMax): 
        if profMax == 0:
            #ter <- terminales
            ter = elegirElemento()