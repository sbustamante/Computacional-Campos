#!/usr/bin/env python
#==========================================================
# DEMOSTRACION 1:
# Bobina fonocaptora
#==========================================================
import numpy as np
import matplotlib.pylab as plt
import AudioLib as ad

#Funcion de oscilacion original
def y(t):
    return y0*np.exp(-t/tau)*np.sin( 2*np.pi*freq1*t )

#Funcion de potencial inducido por bobina fonocaptora
def Vfem(t):
    return (1-y0/L*np.sin( 2*np.pi*freq1*t ))**-4*y0/L*\
    np.exp( -t/tau )*( 2*np.pi*freq1*\
    np.cos( 2*np.pi*freq1*t ) - \
    1/tau*np.sin( 2*np.pi*freq1*t ) )


#CONSTANTES
#Frecuencia fundamental de la cuerda [Hz]
freq1 = 440.
#Amplitud maxima de oscilacion de la cuerda [m]
y0 = 0.002
#Longitud de la cuerda [m]
L = 0.7
#Tiempo de vida medio de una oscilacion [s]
tau = 1.

#Tiempo maximo [s]
tmax = 5
#Intervalos
dt = 1/44100.
#Arreglo de tiempo 
tiempo = np.arange( 0, tmax, dt )

#Potencial
V = Vfem( tiempo )
#Oscilacion original
y_cuerda = y( tiempo )

#Grafica
plt.plot( tiempo, V, linewidth = 0.5 )
plt.grid()
plt.title( "Potencial inducido por una bobina fonocaptora")
plt.xlabel( "t [s]" )
plt.ylabel( "Potential [V_0]" )
plt.show()

#Audio producido por la bobina
nota_bobina = ad.audio()
nota_bobina.load( V*ad.Amplitude/max(V) )
nota_bobina.play()

#Audio original de la cuerda
nota_cuerda = ad.audio()
nota_cuerda.load( y_cuerda*ad.Amplitude/max(y_cuerda) )
nota_cuerda.play()