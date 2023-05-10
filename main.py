#Gregorian catadioptric telescope implementation in Python using matricial (ABCD) raytracing. 
#Firstly, the telescope is compound by one primary mirror and a secondary mirror (both spheric),
#a field lens and an eye-piece. A final image formation lens represents the final phase of the telescope.

"""
Created on Thu May 3 14:30 2023
Modified on Wed May 10 14:19 2023
@authors: Agustín López (alopezz1), Dayana Carmona and Ana Isabel Osorio. Universidad EAFIT, Physics Engineering.
"""

import numpy as np
from ray_tracing_single_lens import *
from functions import *
from PIL import Image, ImageEnhance
#from  scipy.ndimage import gaussian_filter

#Define the optical system parameters
#Optical elements
Rp = 90             #Radius of the primary mirror (mm)
Rs = 36.39          #Raddus of the secondary mirror (mm)
fF = 26.45          #Focal length of the field lens (mm)
fE = 16.21          #Focal length of the eyepiece (mm)
fO = 48             #Focal length of the image formation lens (mm)
#Distance between optical elements
ER = 10.74          #Eye relief (distance between the eyepiece and the eye lens) (mm)
t1 = 68.24          #Spacing between primary and secondary mirror (mm)
t2 = 83.79          #Spacing between secondary mirror and field lens (mm)
t3 = fE             #Spacing between field lens and eyepiece lens (mm)
di = fO             #Image forming distance (mm)

#Optical matrixes generation
#Mirrors matrixes (Reflection)
Mp = optical_matrixes_generator(0, -Rp)             #Primary mirror matrix
Ms = optical_matrixes_generator(0, Rs)              #Secondary mirror matrix 
#Lens matrixes (Refraction)
LF = optical_matrixes_generator(1, fF)              #Field lens matrix 
LE = optical_matrixes_generator(1, fE)              #Eyepiece lens matrix  
LO = optical_matrixes_generator(1, fO)              #Image formation convergent lens matrix 
#Traslation matrixes
T6 = optical_matrixes_generator(2, di)              #Image formation distance matrix 
T5 = optical_matrixes_generator(2, ER)              #Eye relief distance matrix 
T4 = optical_matrixes_generator(2, t3)              #Field lens - Eyepiece distance matrix
T3 = optical_matrixes_generator(2, -t2)             #Secondary Mirror - Field lens distance matrix
T2 = optical_matrixes_generator(2, t1)              #Primary Mirror - Secondary Mirror distance matrix 
T1 = T2                                             #(THIS WAS EQUAL TO T2 BEFORE) Aperture - Primary Mirror distance matrix
#System matrix
S = (T6.dot(LO.dot(T5.dot(LE.dot(T4.dot(LF.dot(T3.dot(Ms.dot(T2.dot(Mp.dot(T1)))))))))))
print("System matrix", S)

#COMPUTING DATA FOR ANALYTICsAL RAY TRACING
#Object distance 
so = 2 * 1e+6
n1 = 1 #Air index of refraction
#Pixel size to real world size conversion
res = 968

#load image (Object!)
input_name = "eiffel.jpg"
obj = Image.open(input_name, 'r')
print("processing" , input_name )
width, height = obj.size
print("width", width, "height", height)

#New image size, no trasveral magnification within the optical system
width_output = int(width*(abs(1)))
height_output = int(height*(abs(1)))
print("width_o", width_output, "height_o", height_output)

#Create new Image and a Pixel Map
image = Image.new("RGB", (width_output, height_output), "white")
pixels = image.load()

#Compute the image with principal ray
pixels = ray_tracing(width, height, 0, n1, so, obj, res, pixels, S, width_output, height_output)

#Compute the acummulated image with parallel ray
pixels = ray_tracing(width, height, 1, n1, so, obj, res, pixels, S, width_output, height_output)

#Interpolate if necesarry
interpolate = True
if interpolate:
  pixels = interpolation(pixels, width_output, height_output)
  print ("Interpolation performed")
  pass
else: print("no interpolation")

#Save Images to File
output_name = "eiffel_output.png"
image.save(output_name, format='PNG')
print("processed image saved as" , output_name )



