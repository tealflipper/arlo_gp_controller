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
def MF(s):
    print("Move forward")

"""
Move forward 1, 2 y 3, el robot se mueve hacia delante con 
con una velodcidad establecida
toma la lista lecturas de sensores s como entrada
regresa un valor para avanzar, solamente en el la ultima condicion 
avanzar
"""
def MF1(s=None):
    print("Move forward 1")
    return 1

def MF2(s=None):
    print("Move forward 2")
    return 2

def MF3(s=None):
    print("Move forward 3")
    return 3

"""
Turn left, el robot gira a la izquierda 30°
toma la lista lecturas de sensores s como entrada
regresa el valor del sensor
"""
def TL(s=None):
    print("Turn left")

"""
Turn right, el robot gira a la derecha 30°
toma la lista lecturas de sensores s como entrada
regresa el valor del sensor
"""
def TR(s=None):
    print("Turn right")

"""
If bump, detecta si el robot esta esta chocando contra algo
Requiere de dos argumentos, si esta chocando se evalua el primero
si no, se evalua el segundo
"""
def IFBMP(arg1=None, arg2=None):
    pass

"""
If stuck, detecta si el robot esta atascado
Requiere de dos argumentos, si esta atascado se evalua el primero
si no, se evalua el segundo
""" 
def IFSTK(arg1=None, arg2=None):
    pass

"""
If less than or equal, condicion A <= B.
Requiere de cuatro argumentos. Hace la
comparacion entre los primeros dos argumentos. Si es 
cierta, se ejecuta el tercer argumento. Si no se ejecuta el cuarto
argumento
"""
def IFLTE(arg1=None, arg2=None, arg3=None, arg4=None):
    #return arg3 if arg1 <= arg2 else arg4
    return 30

"""
Toma como entrada dos argumentos, los evalua y regresa el segundo
"""
def PROGN2(arg1=None, arg2=None):
    return arg2

"""
Entrada: un arbol a y una lista de sensores s
Salida: indentificador para las funciones MF1, MF2 o MF3
"""

class Nodo:
    __1m = 1.0
    __2m = 2.0
    __5m = 5.0
    def __init__(self, hijos, dato, tipoDato=None):
        #self.padre = padre 
        self.hijos = hijos
        self.dato = dato
        self.tipoDato = tipoDato
    
import random     

#un arbol se puede representar con el nodo raiz, por eso hereda de él
class Arbol(Nodo):
    #lista de terminales para el primer experimento
    listaTerminales = (MF1, MF2, MF3)
    listaFuciones = (IFBMP, IFSTK, IFLTE, PROGN2)
    def __init__(self, raiz=None):
        self.raiz = None
        if raiz : 
            self.raiz = raiz


    #metodo para elegir una terminal aleatoria
    def __elegirElemento(self, lista):
        return random.choice(lista)

    """
    crea un arbol completo con profMax de niveles y todos las hojas al mismo nivel
    metodo privado
    """
    def __crearArbolCompleto(self, profMax): 
        if profMax == 0:
            #ter <- terminales
            ter = self.__elegirElemento(self.listaTerminales)
            # nodo raiz
            return Nodo(None,ter)
            
        else:
            fun = self.__elegirElemento(self.listaFuciones)
            hijos= [self.__crearArbolCompleto(profMax-1),self.__crearArbolCompleto(profMax-1)]
            return Nodo(hijos, fun)

    #metodo publico para crear el arbol completo
    def crearArbolCompleto(self, profmax):
        self.raiz = self.__crearArbolCompleto(profMax=profmax)

    """
    crea un arbol acotado con profMax de niveles, en cualquier nivel puede aparecer 
    una hoja o nodo terminal
    metodo privado
    """
    def __crearArbolAcotado(self, profMax): 
        tipoNodo={"FUN":0, "TERM":1}
        choice = random.randint(0, 1) # 0  es funcion, 1 es terminal
        if profMax == 0 or choice == tipoNodo["TERM"]:
            #ter <- terminales
            ter = self.__elegirElemento(self.listaTerminales)
            # nodo raiz
            return Nodo(None,ter)
        else:
            fun = self.__elegirElemento(self.listaFuciones)
            hijos= [self.__crearArbolAcotado(profMax-1),self.__crearArbolAcotado(profMax-1)]
            return Nodo(hijos, fun)
    #metodo publico para crear un arbol acotado
    def crearArbolAcotado(self, prof):
       self.raiz = self.__crearArbolAcotado(prof)

    """
    Metodo privado que imprime el arbol en post orden
    """
    def __imprimirPostorden(self, arbol, nivel = 0):
        if arbol != None: #si nodo existe
            
            if arbol.hijos!=None: 
                for i in range (len(arbol.hijos)):
                    self.__imprimirPostorden(arbol.hijos[i], nivel+1)
            print("\t"*nivel, nivel, arbol.dato)

    def imprimirPostorden(self):
        print("\n\n")
        self.__imprimirPostorden(self.raiz)
    
    """
    Interpretación del arbol en post orden
    """
    def __valor(self, dato):
        return dato

    def __aplicar(self, dato, valorI=None, valorD=None):
        if valorD != None and valorI != None:
            #print("función ", dato.__name__,valorI,valorD)
            return dato()
        else:
            #print("expresión", dato.__name__)
            return dato(None)

    def __interpretar(self,nodo):
        if nodo.hijos == None: #hoja
            if isinstance(nodo.dato, int): # or nodo.tipoDato == "var":
                return self.__valor(nodo.dato)
            else:
                self.__aplicar(nodo.dato)
        else: #recorrer rama izquierda, derecha y aplicar funcion
            valorI = self.__interpretar(nodo.hijos[0])
            valorD = self.__interpretar(nodo.hijos[1])
            return self.__aplicar(nodo.dato, valorI, valorD)

    def interpretar(self):
        print("\n\n")
        self.__interpretar(self.raiz)
        