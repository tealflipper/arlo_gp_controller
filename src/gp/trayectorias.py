#!/usr/bin/env python3
#---------------------------------------------------------Trayectoria Obstaculo--------------------------------------------------------
# license removed for brevity
import rospy
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import isinf
import message_filters
from numpy import linalg as LA
import math
import timeit
from time import time as taim
import time
from numpy import linalg as LA
import math


#sensors
rangosF = np.zeros(shape = (32,1)) #front
rangosL = np.zeros(shape = (32,1)) #left
rangosR = np.zeros(shape = (32,1)) #right

# referencia a documento de matemáticas
#tiempo en el que esta el tramo, tal vez sean constantes 
tp = 3 
tfin_p = 6 #Punto donde comienza el 3er tramo
tfin = 9 #Punto en el tiempo donde se termina de recorrer la trayectoria



#----------------------------------------Primer tramo-----------------------------------------------------------------




# 1) los valores d1 y d2, por ejemplo (2, 2) o (3, 1). Ese valor determina 
#qué rápido alcanza el robot su velocidad final en la curva C1. Si fuera (1, 1) la velocidad sería, 1m/s, 2m/s, 3m/s.
d1 = 0.5
d2 = 0.5

#2) también debes definir la función x(t). En el documento que mandó el prof. 
#Franco sugiere la función x(t) = Vinicial * t + 2w t^2.  
#Acá Vinicial y w son constantes escalares (un número, pues) dadas por tí.
#V1 = Vi

Vi = 1.5
w  = 0.01
#theta = 0 #ángulo de desviación para esquivar el obstáculo (debe estar en el intervalo (0, π/2) en radianes).


def fx1(t):
    return Vi*t + (2*w) * (t)**2
    #return Vi*t + (((w)*(t)**2)/2)

def d1x1(t):
    #return Vi + (t*w)
    return Vi + 4*t*w #dt
    #return t         #dVi
    #return 2* (t)**2 #dw

#Constantes
A = 0.09
a1 = 0
b1 = math.sqrt( ( Vi / (abs(d1x1(0)))  ) ** 2  - 1)
#Version reporte
#c1 = ( (d2 - (b1*d1)) / 2*d1x1(0) )
#Version Franco
c1 = (math.sqrt ( (A/2) - w**2) )/Vi**2




def fy1(t):
    return (c1 * (fx1(t))**2)


def C1(t):
    return np.array ([fx1(t), fy1(t)])


def tramo1(t):
    x1 = fx1(t)
    y1 = fy1(t)
    x2 = fx1(t+0.5)
    y2 = fy1(t+0.5)


    #print("f(t): ",y1, "f(t+x): ",y2)
    #x1, y1 inicial | x2, y2 final 
    vector = np.array ([x2-x1, y2-y1])

    #global theta

    #print(vector)
    magnitud = LA.norm(vector)
    #print("M: ",magnitud)
    angulo = math.degrees(math.atan((y2-y1)/(x2-x1)))
    


    angulo = (math.pi * (angulo))/180

    theta = angulo
    #print("Valor de theta: ", theta)


    #   print("A: ",angulo)
    vl = magnitud/3
    va = (angulo)/3

    return np.array ([vl, va])


#-----------------------------------------------------Segundo tramo----------------------------------------------------

#tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
Beta = 2*c1*fx1(tp)

def fx2(t):
    #return fx1(tp) + (Vi + ((w*tp)/2)*t)
    #global theta
    global tp
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    #Beta = 2*c1*fx1(tp)


    return fx1(tp) + (Vi + (2*w*tp))*t

def fy2(t):
    #global theta
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    global tp
    #Beta = 2*c1*fx1(tp)
    return fy1(tp) + (Beta * ( fx2(t) - fx1(tp)))

def C2(t):
    #global theta
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    global tp
    #Beta = 2*c1*fx1(tp)
    return np.array ([fx2(t), fy2(t)])

def tramo2(t):
    x1 = fx2(t)
    y1 = fy2(t)
    x2 = fx2(t+0.5)
    y2 = fy2(t+0.5)

    #print("f(t): ",y1, "f(t+x): ",y2)
    #x1, y1 inicial | x2, y2 final 
    vector = np.array ([x2-x1, y2-y1])

    #global theta
    global tp
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    
    #Beta = 2*c1*fx1(tp)
    ##global theta
    #print("Valor de theta2: ", theta[0])

    #print(vector)
    magnitud = LA.norm(vector)
    #print("M: ",magnitud)
    angulo = math.degrees(math.atan((y2-y1)/(x2-x1)))
    #print("A: ",angulo)

    angulo = (math.pi * (angulo))/180
    
    vl = magnitud/3
    va = (angulo)/3

    return np.array ([vl, 0]) #Regresamos 0 en la va pues es un movimiento rectilineo uniforme


#-----------------------------------------------Tercer Tramo----------------------------------------------------------

#Si comenzamos con fx1 y fy1 se obtienen los resultados de la primera curva pero invertidos
def fx3(t):
    global tfin
    global p
    global tfin_p
    #global theta
    global tp
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    #Beta = 2*c1*fx1(tp)
    return fx1(tfin_p) + fx1(tp) - fx1(tp - t) 


def fy3(t):
    global tfin
    global p
    global tfin_p
    #global theta
    global tp
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    #Beta = 2*c1*fx1(tp)
    return fy1(tfin_p) + fy1(tp) - fy1(tp - t)


def C3(t):
    return np.array ([fx3(t), fy3(t)])

def tramo3(t):
    x1 = fx3(t)
    y1 = fy3(t)
    x2 = fx3(t+0.5)
    y2 = fy3(t+0.5)

    #print("f(t): ",y1, "f(t+x): ",y2)
    #x1, y1 inicial | x2, y2 final 
    vector = np.array ([x2-x1, y2-y1])

    #global theta
    global tp
    #tp = ((-c1*Vi) + math.sqrt( (c1**2)*(Vi**2) + 2*c1*w*math.tan(theta) )) / (2*c1*w) 
    #Beta = 2*c1*fx1(tp)

    #print(vector)
    magnitud = LA.norm(vector)
    #print("M: ",magnitud)
    angulo = math.degrees(math.atan((y2-y1)/(x2-x1)))
    #print("A: ",angulo)

    angulo = (math.pi * (angulo))/180
    
    vl = magnitud/3
    va = ((angulo)/3) * -1

    return np.array ([vl, va]) 















#---------------------------------------------------


def callbackObstaculo(scanner_center,scanner_left, scanner_right):
    global rangosF
    global rangosL
    global rangosR
    rangosF = scanner_center.ranges
    rangosL = scanner_left.ranges
    rangosR = scanner_right.ranges 


def controlarRobotObstaculo():

   global rangosF
   global rangosL
   global rangosR

   # Crear publicador para el tópico de las llantas del robot.
   pubVel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

   # Cuántas iteraciones por segundo hará el siguiente ciclo.
   # Es decir, qué tan frecuente se mandarán los comandos (velocidades) al robot.
   rate = rospy.Rate(2)  # 10hz: 10 veces por segundo de simulación NO segundos de tiempo real


   t = 0
   t2 = 0
   t3 = 0
   retraso = 0
   while not rospy.is_shutdown():
      if(retraso > 4 or not(isinf(rangosF[16])) ):
          vel_msg = Twist()
          if( (isinf(rangosF[16]) and isinf(rangosR[16])) and t >= 8 ): #or rangosF[16]>2.5
            if(t>=8 and t<11):
                print("----Tramo4 ----")
                vel_msg.linear.x, vel_msg.angular.z = tramo1(t2)
                vel_msg.angular.z = vel_msg.angular.z *(-1)   
                t2 = t2 + 0.5 
                t = t + 0.5       
            elif(t>=8 and t<13):
                print("----Tramo5----")
                vel_msg.linear.x, vel_msg.angular.z = tramo2(t2)
                vel_msg.angular.z = vel_msg.angular.z *(-1)  
                t2 = t2 + 0.5
                t = t + 0.5

            elif(t>=8 and t<16):
                print("----Tramo6----")
                vel_msg.linear.x, vel_msg.angular.z = tramo3(t3)
                vel_msg.angular.z = vel_msg.angular.z 
                t3 = t3+0.5
                t = t + 0.5
            elif(t>=8 and t>=16):
                print("----Se acabo la trayectoria----")
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0
                t = t + 0.5
            else:
                vel_msg.linear.x = 0.4
                vel_msg.angular.z = 0
                t = t + 0.5
          else:

            if(t<3):
                print("----Tramo1----")
                vel_msg.linear.x, vel_msg.angular.z = tramo1(t) 
            elif (t<5):
                print("----Tramo2----")
                vel_msg.linear.x, vel_msg.angular.z = tramo2(t)
            elif (t<8):
                print("----Tramo3----")
                vel_msg.linear.x, vel_msg.angular.z = tramo3(t3)
                t3 = t3+0.5
            t = t + 0.5
      else:
        print("--Retraso--")
        vel_msg.linear.x = 0.3
        vel_msg.angular.z = 0  
        t = 0
        retraso = retraso + 1  



      pubVel.publish(vel_msg)
      print("Vl: ", vel_msg.linear.x, "Va: ", vel_msg.angular.z )
      print("SensorF: ", rangosF[16])
      print("t: ", t)
      rate.sleep()


# if __name__ == '__main__':
#     try:
#         rospy.init_node('prueba_robot', anonymous=True)
#         # Para cuando ya necesites tener información de Gazebo hacia tu nodo (p.ej. sensores),
#         # en algún punto de acá te debes suscribir al tópico y poner qué función se 
#         # llamará cada que llegue un mensaje.


#         scanner_center= message_filters.Subscriber('/arlo/laser/scan_center', LaserScan)
#         scanner_left = message_filters.Subscriber('/arlo/laser/scan_left', LaserScan)
#         scanner_right = message_filters.Subscriber('/arlo/laser/scan_right', LaserScan)

#         ts = message_filters.TimeSynchronizer([scanner_center, scanner_left, scanner_right], 10)
#         ts.registerCallback(callbackObstaculo)


#         #Se llama al controlador del robot
#         controlarRobotObstaculo()
#     except rospy.ROSInterruptException:
#         pass

#--------------------------------------------------Trayectoria Giro a la Izquierda-----------------------------------


#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import isinf
import message_filters
from numpy import linalg as LA
import timeit
from time import time as taim
import time
import math



rangosF = np.zeros(shape = (32,1))
rangosL = np.zeros(shape = (32,1))
rangosR = np.zeros(shape = (32,1))



def funcion1Right(t):
    return -(0.3 + ((-1.5-0.3)/(1+(t/0.1)**2.4)))

def getVelRight(t):
    x1 = t
    y1 = funcion1Right(x1)
    x2 = x1 + 0.5
    y2 = funcion1Right(x2)
    
    vector = np.array ([x2-x1, y2-y1])

    #print(vector)
    magnitud = LA.norm(vector)
    #print("M: ",magnitud)
    angulo = math.degrees(math.atan((y2-y1)/(x2-x1)))
    #print("A: ",angulo)

    angulo = (math.pi * (90-angulo))/180
    
    vl = magnitud/3
    va = (angulo)/3
    v = np.array ([vl, va])
    return v

def funcion1(t):
    return 0.3 + ((-1.5-0.3)/(1+(t/0.1)**2.4))

def getVel(t):
    x1 = t
    y1 = funcion1(x1)
    x2 = x1 + 0.5
    y2 = funcion1(x2)
    
    vector = np.array ([x2-x1, y2-y1])

    #print(vector)
    magnitud = LA.norm(vector)
    #print("M: ",magnitud)
    angulo = math.degrees(math.atan((y2-y1)/(x2-x1)))
    #print("A: ",angulo)

    angulo = (math.pi * (90-angulo))/180
    
    vl = magnitud/3
    va = (angulo)/3
    v = np.array ([vl, va])
    return v


def callback(scanner_center,scanner_left, scanner_right):
    global rangosF
    global rangosL
    global rangosR
    rangosF = scanner_center.ranges
    rangosL = scanner_left.ranges
    rangosR = scanner_right.ranges 



def vueltaDerecha():

   global rangosF
   global rangosL
   global rangosR


   pubVel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
   vel_msg = Twist()

   rate = rospy.Rate(50) 

   while not rospy.is_shutdown():

     

    if(isinf(rangosF[16])):
        vel_msg.linear.x = 0.4
        vel_msg.angular.z = 0.0
        pubVel.publish(vel_msg)

        print("not turning anymore")
        break
        if(isinf(rangosL[16]) and isinf(rangosR[16])):
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            print("not moving anymore")


    else:

        print("rango menor a un metro, vuelta")
        print(rangosF[16], rangosL[16], rangosR[16])
        if((rangosF[16]<=0.16 or rangosL[16] <= 0.20 or rangosR[16] <= 0.20 )): 
            print("robot atorado")
            break
        if(rangosF[16]<1.2): 
          vel_msg.linear.x, vel_msg.angular.z = getVelRight(0.5)
        else:
            print("Se detecto")
            vel_msg.linear.x, vel_msg.angular.z = getVelRight(0)


    pubVel.publish(vel_msg)
    print("Vl: ", vel_msg.linear.x, "Va: ", vel_msg.angular.z )
    rate.sleep()

def controlarRobot():

   global rangosF
   global rangosL
   global rangosR


   pubVel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
   vel_msg = Twist()

   rate = rospy.Rate(50) 

   while not rospy.is_shutdown():

     

    if(isinf(rangosF[16])):
        vel_msg.linear.x = 0.4
        vel_msg.angular.z = 0.0
        pubVel.publish(vel_msg)

        print("not turning anymore")
        break
        if(isinf(rangosL[16]) and isinf(rangosR[16])):
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            print("not moving anymore")


    else:

        print("rango menor a un metro, vuelta")
        print(rangosF[16], rangosL[16], rangosR[16])
        if((rangosF[16]<=0.16 or rangosL[16] <= 0.20 or rangosR[16] <= 0.20 )): 
            print("robot atorado")
            break
        if(rangosF[16]<1.2): 
          vel_msg.linear.x, vel_msg.angular.z = getVel(0.5)
        else:
            print("Se detecto")
            vel_msg.linear.x, vel_msg.angular.z = getVel(0)


    pubVel.publish(vel_msg)
    print("Vl: ", vel_msg.linear.x, "Va: ", vel_msg.angular.z )
    rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('trayectoria_robot', anonymous=True)

        scanner_center= message_filters.Subscriber('/arlo/laser/scan_center', LaserScan)
        scanner_left = message_filters.Subscriber('/arlo/laser/scan_left', LaserScan)
        scanner_right = message_filters.Subscriber('/arlo/laser/scan_right', LaserScan)

        ts = message_filters.TimeSynchronizer([scanner_center, scanner_left, scanner_right], 10)
        ts.registerCallback(callback)

        controlarRobot()
    except rospy.ROSInterruptException:
        pass

def turnLeft():
    try:
        scanner_center= message_filters.Subscriber('/arlo/laser/scan_center', LaserScan)
        scanner_left = message_filters.Subscriber('/arlo/laser/scan_left', LaserScan)
        scanner_right = message_filters.Subscriber('/arlo/laser/scan_right', LaserScan)

        ts = message_filters.TimeSynchronizer([scanner_center, scanner_left, scanner_right], 10)
        ts.registerCallback(callback)

        controlarRobot()
    except rospy.ROSInterruptException:
        pass

def turnRight():
    try:
        scanner_center= message_filters.Subscriber('/arlo/laser/scan_center', LaserScan)
        scanner_left = message_filters.Subscriber('/arlo/laser/scan_left', LaserScan)
        scanner_right = message_filters.Subscriber('/arlo/laser/scan_right', LaserScan)

        ts = message_filters.TimeSynchronizer([scanner_center, scanner_left, scanner_right], 10)
        ts.registerCallback(callback)

        vueltaDerecha()
    except rospy.ROSInterruptException:
        pass


