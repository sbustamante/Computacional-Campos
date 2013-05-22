#!/usr/bin/env python
#==========================================================
# DEMOSTRACION 3: Parte 1
# Solucion numerica de problema de 3 cuerpos 
# electrostaticos
#==========================================================
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
from RungeKutta4 import rk4_step

#Ecuaciones de movimiento
def dF(Y, t):
    #Posicion X particula 1
    x1 = Y[0]
    #Posicion Y particula 1
    y1 = Y[1]
    #Velocidad X particula 1
    vx1 = Y[2]
    #Velocidad Y particula 1
    vy1 = Y[3]
    
    #Posicion X particula 2
    x2 = Y[4]
    #Posicion Y particula 2
    y2 = Y[5]
    #Velocidad X particula 2
    vx2 = Y[6]
    #Velocidad Y particula 2
    vy2 = Y[7]
    
    #Posicion X particula 3
    x3 = Y[8]
    #Posicion Y particula 3
    y3 = Y[9]
    #Velocidad X particula 3
    vx3 = Y[10]
    #Velocidad Y particula 3
    vy3 = Y[11]
    
    #Modulo distancia entre particula 1 y 2
    r12 = np.linalg.norm( [x1-x2, y1-y2] )
    #Modulo distancia entre particula 1 y 3
    r13 = np.linalg.norm( [x1-x3, y1-y3] )
    #Modulo distancia entre particula 2 y 3
    r23 = np.linalg.norm( [x2-x3, y2-y3] )
    
    #Derivada dx/dt particula 1
    dx1 = vx1
    #Derivada dy/dt particula 1
    dy1 = vy1
    #Derivada d vx/dt particula 1
    dvx1 = q1/(4*np.pi*eps0*m1)*( q2/r12**3*(x1-x2) + \
    q3/r13**3*(x1-x3) )
    #Derivada d vy/dt particula 1
    dvy1 = q1/(4*np.pi*eps0*m1)*( q2/r12**3*(y1-y2) + \
    q3/r13**3*(y1-y3) )
    
    #Derivada dx/dt particula 2
    dx2 = vx2
    #Derivada dy/dt particula 2
    dy2 = vy2
    #Derivada d vx/dt particula 2
    dvx2 = q2/(4*np.pi*eps0*m2)*( q1/r12**3*(x2-x1) + \
    q3/r23**3*(x2-x3) )
    #Derivada d vy/dt particula 2
    dvy2 = q2/(4*np.pi*eps0*m2)*( q1/r12**3*(y2-y1) + \
    q3/r23**3*(y2-y3) )
    
    #Derivada dx/dt particula 3
    dx3 = vx3
    #Derivada dy/dt particula 3
    dy3 = vy3
    #Derivada d vx/dt particula 3
    dvx3 = q3/(4*np.pi*eps0*m3)*( q1/r13**3*(x3-x1) + \
    q2/r23**3*(x3-x2) )
    #Derivada d vy/dt particula 3
    dvy3 = q3/(4*np.pi*eps0*m3)*( q1/r13**3*(y3-y1) + \
    q2/r23**3*(y3-y2) )

    #Derivadas
    return np.array([ dx1, dy1, dvx1, dvy1, \
    dx2, dy2, dvx2, dvy2, \
    dx3, dy3, dvx3, dvy3 ])
    

#CONSTANTES
#Permitividad del vacio
eps0 = 8.85418e-12
#Ancho de la mesa
ancho = 1.2
#Largo de la mesa
largo = 2.4

#CONDICIONES BOLA 1
#masa
m1 = 0.1
#carga
q1 = 5e-5
#radio 
r1 = 0.05
#posicion inicial
x10 = 0.1
y10 = 0.1
#velocidad inicial
vx10 = 5.0
vy10 = 5.0

#CONDICIONES BOLA 2
#masa
m2 = 0.1
#carga
q2 = 5e-5
#radio 
r2 = 0.05
#posicion inicial
x20 = 0.3
y20 = 0.1
#velocidad inicial
vx20 = -5.0
vy20 = 5.0

#CONDICIONES BOLA 3
#masa
m3 = 0.1
#carga
q3 = 5e-5
#radio 
r3 = 0.05
#posicion inicial
x30 = 0.2
y30 = 0.2
#velocidad inicial
vx30 = -1.0
vy30 = 5.0

#INTEGRACION DEL SISTEMA
#tiempo maximo a integrar
t_max = 10
#salto del tiempo
t_step = 0.001
#condiciones iniciales
cond_ini = [ x10, y10, vx10, vy10, \
x20, y20, vx20, vy20, \
x30, y30, vx30, vy30]
#tiempo de evaluacion
tiempo = np.arange( 0, t_max, t_step )
#integracion del sistema
solucion = []
Y = cond_ini
for t in tiempo:
    Y = rk4_step( dF, Y, t, t_step )
    #Condiciones de colision con la mesa
    if Y[0] < r1 or Y[0] >= ancho-r1:
	Y[2] = -Y[2]
    if Y[4] < r2 or Y[4] >= ancho-r2:
	Y[6] = -Y[6]
    if Y[8] < r3 or Y[8] >= ancho-r3:
	Y[10] = -Y[10]
	
    if Y[1] < r1 or Y[1] >= largo-r1:
	Y[3] = -Y[3]
    if Y[5] < r2 or Y[5] >= largo-r2:
	Y[7] = -Y[7]
    if Y[9] < r3 or Y[9] >= largo-r3:
	Y[11] = -Y[11]

    solucion.append( Y )

#resultado de integracion
x1_t, y1_t, vx1_t, vy1_t, \
x2_t, y2_t, vx2_t, vy2_t, \
x3_t, y3_t, vx3_t, vy3_t = \
np.transpose( solucion )

#Guardando archivo de datos
np.savetxt( 'trayectorias.txt', np.transpose([tiempo,\
x1_t, y1_t, x2_t, y2_t, x3_t, y3_t]) )

#Grafica de trayectorias
plt.plot( x1_t, y1_t, label='particula 1' )
plt.plot( x2_t, y2_t, label='particula 2')
plt.plot( x3_t, y3_t, label='particula 3')

#Formato de grafica
plt.xlim( (0,ancho) )
plt.ylim( (0,largo) )
plt.grid()
plt.legend()
plt.show()