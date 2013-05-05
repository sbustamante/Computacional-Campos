#!/usr/bin/env python
#==========================================================
# EJEMPLO DE USO
# Grafica de funciones y datos aleatorios
#==========================================================
import numpy as np
import scipy as sp
import matplotlib.pylab as plt

#Funcion 1
def Funcion1(x):
    f1 = np.sin(x)/( np.sqrt(1 + x**2) )
    return f1
    
#Funcion 2
def Funcion2(x):
    f2 = 1/(1+x)
    return f2
    
#Valores de x para evaluar
X = np.linspace( 0, 10, 100 )
#Evaluacion de funcion 1
F1 = Funcion1(X)
#Evaluacion de funcion 2
F2 = Funcion2(X)

#Grafica funcion 1
plt.plot( X, F1, label='Funcion 1' )
#Grafica funcion 2
plt.plot( X, F2, label='Funcion 2' )

#Datos aleatorios eje Y
Yrand = sp.random.rand( 100 )
#Grafica datos aleatorios
plt.plot( X, Yrand, 'o', label='Datos' )

plt.legend()
plt.show()