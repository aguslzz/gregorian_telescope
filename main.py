#Gregorian catadioptric telescope implementation in Python using matricial (ABCD) raytracing.
#The design of the optical system is described in the pdf Gregorian-Telescope1.
#Firstly, the telescope is compoun by one primary mirror (Concave-Paraboloid) and a secondary mirror (Concave-Ellipsoid)
#a field lens (Bi-concave) and an eye lens (Bi-concave) represent the final phase of the image formation.


import numpy as np

#Define the optical system parameters
#Optical elements
Rp = -90            #Radius of the primary mirror (mm)
Rs = 36.39          #Raidus of the secondary mirror (mm)
fF = 26.45          #Focal length of the field lens (mm)
fE = 10.21          #Focal length of the eye lens (mm)
fO = 18.78          #Focal length of the ocular eye lens (mm)
#Distance between optical elements
ER = 10.74          #Eye relief (distance between the eye lens to the tip of your eye) (mm)
t1 = 68.24          #Spacing between primary and secondary mirror (mm)
t2 = 83.79          #Spacing between secondary mirror and field lens (mm)
t3 = 16.21          #Spacing between field lens and eye lens (mm)
di = fO

#ABCD matricial raytracing
#Mirrors matrixes 
Mp = np.matrix([[-1, -2/Rp], [0, 1]])           #Primary mirror matrix (reflection)
Ms = np.matrix([[-1, -2/Rs], [0, 1]])           #Secondary mirror matrix (reflection)
#lens matrixes
LF = np.matrix([[1, -1/fF], [0, 1]])            #Field lens matrix (refraction)
LE = np.matrix([[1, -1/fE], [0, 1]])            #Eye lens matrix (refraction)
LO = np.matrix([[1, -1/fO], [0, 1]])            #Image formation convergent lens matrix (refraction)
#Traslation matrixes
T6 = np.matrix([[1, 0], [di, 1]])               #Image formation distance matrix (traslation)
T5 = np.matrix([[1, 0], [ER, 1]])               #Eye relief distance matrix (traslation)
T4 = np.matrix([[1, 0], [t3, 1]])               #Eye relief distance matrix (traslation)
T3 = np.matrix([[1, 0], [t2, 1]])               #Eye relief distance matrix (traslation)
T2 = np.matrix([[1, 0], [t1, 1]])               #Eye relief distance matrix (traslation)
T1 = T2
#System matrix
S = T6*LO*T5*LE*T4*LF*T3*Ms*T2*Mp*T1

print(S)

