import numpy as np

a=float(input('give value of lattice constant for the crystal in cm ='))

wavelength = float(input('give the wavelength of the light incident on the crystal in cm = '))

h_cross=1.0545718*(10**(-34))

K=(2*np.pi)/wavelength

G = (2*(3**(1/2))*np.pi)/a

final_momentum = (K+G)*h_cross
   
print (" The final momentum of the system is = ",final_momentum)
