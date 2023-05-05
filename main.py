#Gregorian catadioptric telescope implementation in Python using matricial (ABCD) raytracing. 
#The design of the optical system is described in the pdf Gregorian-Telescope1.
#Firstly, the telescope is compoun by one primary mirror (Concave-Paraboloid) and a secondary mirror (Concave-Ellipsoid)
#a field lens (Bi-concave) and an eye lens (Bi-concave) represent the final phase of the image formation.

"""
Created on Thu May 23 14:30 2023
@authors: Agustín López (alopezz1), Dayana Carmona and Ana Isabel Osorio. Universidad EAFIT, Physics Engineering.
"""


import numpy as np
from ray_tracing_single_lens import *
from functions import *
#from  scipy.ndimage import gaussian_filter

#Define the optical system parameters
#Optical elements
Rp = 90             #Radius of the primary mirror (mm)
Rs = 36.39          #Raidus of the secondary mirror (mm)
fF = 26.45          #Focal length of the field lens (mm)
fE = 10.21          #Focal length of the eye lens (mm)
fO = 18.78          #Focal length of the ocular eye lens (mm)
#Distance between optical elements
ER = 10.74          #Eye relief (distance between the eyepiece and the eye lens) (mm)
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
#S = np.array([[-3.79e-2, -3.93e1], [-7.60e-2, -5.24e1]])
print("System matrix", S)

#COMPUTING DATA FOR ANALYTICAL RAY TRACING
#Object distance (in meters)
so = 0.0012
#Image distance (in meters)
si = 0.003

n1 = 1 #Air index of refraction 

#Magnification
Mt = si /so
Mt = 1.1
print ("Mt: ", Mt)

#Pixel size to real world size conversion
res = 0.0001 #each pixel equals 0.1 mm

#load image (Object!)
obj = Image.open('landscape.jpg', 'r')
width, height = obj.size

width_output = int(width*(abs(Mt)))
height_output = int(height*(abs(Mt)))

# Create new Image and a Pixel Map
image = Image.new("RGB", (width_output, height_output), "white")
pixels = image.load()

#Compute the image with chief ray
pixels = ray_tracing(width, height, 0, n1, so, obj, res, pixels, S, width_output, height_output)

#Compute the cummulated image with parallel ray
pixels = ray_tracing(width, height, 1, n1, so, obj, res, pixels, S, width_output, height_output)

print("this is before interpolation")
#Interpolate if necesarry
if (np.abs(Mt) > 1.0):
  pixels = interpolation(pixels, width_output, height_output)
  print ("Interpolation performed")
  pass
else: print("no interpolation")

#Save Images to File
output_name = "landscape_output.png"
image.save(output_name, format='PNG')
print("image saved as" , output_name )


