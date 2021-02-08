from arlo_gp_controller import Arbol
from arlo_gp_controller import imprimirPostorden

a = Arbol ()
a = a.crearArbolCompleto(2)

print (len(a.hijos[0].hijos), a.hijos[0].dato,a.hijos[0].hijos[1].dato)
imprimirPostorden(a)
