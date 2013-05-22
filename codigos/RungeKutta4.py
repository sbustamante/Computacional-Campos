#!/usr/bin/env python
import numpy as np

#==========================================================
# RUNGE KUTTA 4
# Metodo de integracion numerica Runge Kutta 4
# Argumentos:
# Funcion dinamica, condicion inicial, arreglo de tiempos
# y paso de integracion
#==========================================================
def rk4_step( odesys, Yini, t, h ):
  
    k1 = odesys( Yini, t )
    k2 = odesys( Yini+0.5*h*k1, t+0.5*h )
    k3 = odesys( Yini+0.5*h*k2, t+0.5*h )
    k4 = odesys( Yini+h*k3    , t+h )
    Y = Yini + h*(k1+2*k2+2*k3+k4)/6
    
    return Y