#!/usr/bin/env python
#==========================================================
# DEMOSTRACION 3: Parte 2
# Solucion numerica de problema de 3 cuerpos 
# electrostaticos. Animacion 3D
#==========================================================
import numpy as np
import tvtk.tools.visual as visual

#Cargando datos de las bolas
tiempo, x1_t, y1_t, x2_t, y2_t, x3_t, y3_t = \
np.transpose( np.loadtxt('trayectorias.txt') )

#CONSTANTES
#Ancho de la mesa
ancho = 1.2
#Largo de la mesa
largo = 2.4
#Grosor de los muros del billar
grosor = 0.1
#Radio bola 1
r1 = 0.05
#Radio bola 2
r2 = 0.05
#Radio bola 3
r3 = 0.05

#Creando bola 1
bola1 = visual.sphere( radius=r1, color=(1.0, 1.0, 1.0) )
bola1.pos = [ 0., 0., 0. ]
bola1.t = 0
bola1.dt = 1

#Creando bola 2
bola2 = visual.sphere( radius=r2, color=(1.0, 1.0, 1.0) )
bola2.pos = [ 0., 0., 0. ]
bola2.t = 0
bola2.dt = 1

#Creando bola 1
bola3 = visual.sphere( radius=r3, color=(1.0, 1.0, 1.0) )
bola3.pos = [ 0., 0., 0. ]
bola3.t = 0
bola3.dt = 1

#Creando mesa
mesa = visual.box( pos=(ancho/2., largo/2., -grosor/2.), \
size=(ancho, largo, grosor), color=(0.0, 0.3, 0.0) )

muro_l = visual.box( pos=(-grosor/2., largo/2., 0.0), \
size=(grosor, largo + 2*grosor, grosor), \
color=(0.6, 0.3, 0.0) )
muro_r = visual.box( pos=(ancho+grosor/2., largo/2., 0.0), \
size=(grosor, largo + 2*grosor, grosor), \
color=(0.6, 0.3, 0.0) )
muro_d = visual.box( pos=(ancho/2., -grosor/2., 0.0), \
size=(ancho + 2*grosor, grosor, grosor), \
color=(0.6, 0.3, 0.0) )
muro_u = visual.box( pos=(ancho/2., largo+grosor/2., 0.0), \
size=(ancho + 2*grosor, grosor, grosor), \
color=(0.6, 0.3, 0.0) )


#ITERACION DEL SISTEMA
def anim(): 
    #Evolucion de la bola 1
    bola1.t = bola1.t + bola1.dt
    i = bola1.t
    bola1.pos = visual.vector( x1_t[i], y1_t[i], r1 )
    
    #Evolucion de la bola 2
    bola2.t = bola2.t + bola2.dt
    i = bola2.t
    bola2.pos = visual.vector( x2_t[i], y2_t[i], r2 )
    
    #Evolucion de la bola 3
    bola3.t = bola3.t + bola3.dt
    i = bola3.t
    bola3.pos = visual.vector( x3_t[i], y3_t[i], r3 )

a = visual.iterate(10, anim)
visual.show()