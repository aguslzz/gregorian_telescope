#Gregorian catadioptric telescope implementation in Python using matricial (ABCD) raytracing.
#The design of the optical system is described in the pdf Gregorian-Telescope1.
#Firstly, the telescope is compoun by one primary mirror (Concave-Paraboloid) and a secondary mirror (Concave-Ellipsoid)
#a field lens (Bi-concave) and an eye lens (Bi-concave) represent the final phase of the image formation.


import numpy as np
from ray_tracing_single_lens import *
from functions import *

#Define the optical system parameters
#Optical elements
Rp = 90             #Radius of the primary mirror (mm)
Rs = 36.39          #Raidus of the secondary mirror (mm)
fF = 26.45          #Focal length of the field lens (mm)
fE = 10.21          #Focal length of the eye lens (mm)
fO = 18.78          #Focal length of the ocular eye lens (mm)
#Distance between optical elements
ER = 10.74          #Eye relief (distance between the eye lens to the tip of your eye) (mm)
t1 = 68.24          #Spacing between primary and secondary mirror (mm)
t2 = 83.79          #Spacing between secondary mirror and field lens (mm)
t3 = 16.21          #Spacing between field lens and eyepiece lens (mm)
di = fO             #Image forming distance (mm)

#Optical matrixes generation
#Mirrors matrixes (Reflection)
Mp = optical_matrixes_generator(0, -Rp)              #Primary mirror matrix (reflection)
Ms = optical_matrixes_generator(0, Rs)              #Secondary mirror matrix (reflection)
#Lens matrixes (Refraction)
LF = optical_matrixes_generator(1, fF)              #Field lens matrix 
LE = optical_matrixes_generator(1, fE)              #Eyepiece lens matrix  
LO = optical_matrixes_generator(1, fO)              #Image formation convergent lens matrix 
#Traslation matrixes
T6 = optical_matrixes_generator(2, di)              #Image formation distance matrix 
T5 = optical_matrixes_generator(2, ER)              #Eye relief distance matrix 
T4 = optical_matrixes_generator(2, t3)              #Field lens - Eyepiece distance matrix
T3 = optical_matrixes_generator(2, -t2)              #Secondary Mirror - Field lens distance matrix
T2 = optical_matrixes_generator(2, t1)              #Primary Mirror - Secondary Mirror distance matrix 
T1 = T2                                             #Aperture - Primary Mirror distance matrix
#System matrix
S = (T6.dot(LO.dot(T5.dot(LE.dot(T4.dot(LF.dot(T3.dot(Ms.dot(T2.dot(Mp.dot(T1)))))))))))
print(S)
#Mirrors matrixes 
#Mp = np.matrix([[-1, -2/Rp], [0, 1]])           #Primary mirror matrix (reflection)
#Ms = np.matrix([[-1, -2/Rs], [0, 1]])           #Secondary mirror matrix (reflection)
#lens matrixes
#LF = np.matrix([[1, -1/fF], [0, 1]])            #Field lens matrix (refraction)
#LE = np.matrix([[1, -1/fE], [0, 1]])            #Eye lens matrix (refraction)
#LO = np.matrix([[1, -1/fO], [0, 1]])            #Image formation convergent lens matrix (refraction)
#Traslation matrixes
#T6 = np.matrix([[1, 0], [di, 1]])               #Image formation distance matrix (traslation)
#T5 = np.matrix([[1, 0], [ER, 1]])               #Eye relief distance matrix (traslation)
#T4 = np.matrix([[1, 0], [t3, 1]])               #Eye relief distance matrix (traslation)
#T3 = np.matrix([[1, 0], [t2, 1]])               #Eye relief distance matrix (traslation)
#T2 = np.matrix([[1, 0], [t1, 1]])               #Eye relief distance matrix (traslation)
#T1 = T2
