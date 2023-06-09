#Functions code for main of the gregorian telescope

import numpy as np
import math 
from PIL import Image
from scipy.interpolate import griddata
from scipy import interpolate

## Carlos´ functions

#Interpolation functions within white or non-white pixels
def interpolation (pixels, width_o, height_o):

  arry = np.zeros((width_o, height_o))
  for i in range(width_o):
    for j in range(height_o):
      arry[i,j] = pixels[i,j][0]

  # Get the coordinates of the non-white pixels
  nonwhite_coords = np.argwhere(arry != 255)
  # Get the coordinates of the white pixels
  white_coords = np.argwhere(arry == 255)

  # Get the pixel values of the non-white pixels
  nonwhite_pixels = arry[nonwhite_coords[:,0], nonwhite_coords[:,1]]

  # Interpolate the pixel values of the white pixels
  interpolated_pixels = griddata(nonwhite_coords, nonwhite_pixels, white_coords, method='linear', rescale=True)

  #Change resulting NaN values with some value (zero, for instance)
  interpolated_pixels = np.nan_to_num(interpolated_pixels, nan=127.0)

  #Round interpolated values to integers
  int_out = np.round(interpolated_pixels).astype(int)

  #Fill white pixels locations with interpolated values
  for i in range(int_out.shape[0]):
    pixels[white_coords[i,0], white_coords[i,1] ] = ( int_out[i], int_out[i], int_out[i] )

  #Returne pixels array with interpolated values
  return pixels

#Complex lens matrix generator
def compute_lens_matrix(nl, R1, R2, dl):
    # Power of each interface
    D1 = (nl - 1) / R1
    D2 = (nl - 1) / (-R2)

    # Lens matrix
    a1 = (1 - (D2 * dl) / nl)
    a2 = -D1 - D2 + (D1 * D2 * dl / nl)
    a3 = dl / nl
    a4 = (1 - (D1 * dl) / nl)
    A = np.array([[a1, a2], [a3, a4]])

    return A

#Ray tracing function
def ray_tracing(width, height, rayo, n1, so, obj, res, pixels, transfmatrix, width_o, height_o):
    
    # Iterate over each pixel of the image
    for i in range(width):
        for j in range(height):
            
            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i
            pos_y = j
            pixel = obj.getpixel((pos_x, pos_y))            
            x = pos_x - width/2
            y = pos_y - height/2
            
            # Calculate the distance from the particular pixel to the center of the object (in pixels)
            r = math.sqrt( x*x + y*y ) + 1 #Rounding correction
        
            #Input ray vector (point in the object plane)
            y_objeto = r*res # Conversion to real world coordinates
            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/so) #This ray enters towards the center of the lens
                V_entrada = np.array([n1*alpha_entrada,y_objeto])
            elif rayo == 1: #parallel
                alpha_entrada = 0 #This ray enters parallel to the optical axis
                V_entrada = np.array([n1*alpha_entrada,y_objeto])
            elif rayo == 2: #mid rays
                entry_angles = np.linspace(0, math.atan(y_objeto/so), 20)
                for alpha in entry_angles:
                    V_entrada = np.array([n1*alpha,y_objeto])

            #Output ray vector calculation
            V_salida = transfmatrix.dot(V_entrada)
        
            #Transversal magnification
            y_imagen = V_salida[1]
            if rayo == 0: #principal
                Mt = (1)*y_imagen/y_objeto #atan correction
            elif rayo == 1: #parallel
                Mt = y_imagen/y_objeto
            elif rayo == 2: #mid rays                                         #CAMBIAR CUADRAR (REVISAR CON LÍNEA 83)
                Mt = y_imagen/y_objeto
                            
            #Conversion from image coordinates to lens coordinates        
            x_prime = Mt*x
            y_prime = Mt*y
            pos_x_prime = int(x_prime + width_o/2)
            pos_y_prime = int(y_prime + height_o/2)
            
            if  pos_x_prime < 0 or pos_x_prime >= width_o:
            	continue
            if  pos_y_prime < 0 or pos_y_prime >= height_o:
            	continue 
            if rayo == 0: #principal   
                pixels[pos_x_prime, pos_y_prime] = (int(pixel), int(pixel), int(pixel))
            elif rayo == 1: #parallel    
                new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0])/2
                pix_fin = ( int(new_gray), int(new_gray), int(new_gray) )        
                pixels[pos_x_prime, pos_y_prime] = pix_fin
            elif rayo == 2: #mid ray
                rays_lost = 0
                try:
                    new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0])/2
                except:
                    rays_lost += 1

                    pix_fin = ( int(new_gray), int(new_gray), int(new_gray) )        
                    pixels[pos_x_prime, pos_y_prime] = pix_fin
    return pixels

## My functions

#Matrix formation function
#[type] 0 for mirror, type = 1 for lens and 2 for traslation
#[value] Radii for mirror, focal for lens and distance for traslation
def optical_matrixes_generator(type, value):
#Mirrors matrix
    if type == 0:
        return np.array([[1, 0], [2/value, 1]])
#Lens matrix
    elif type == 1:
        return np.array([[1, 0], [-1/value, 1]])
#Traslation matrix
    elif type == 2:
        return np.array([[1, value], [0, 1]])
    else: return np.array([[0, 0], [0, 0]])

#Magnification for each ray in the correspondent pixel
def get_magnification(width, height, rayo, n1, so, res, transfmatrix):
    # Iterate over each pixel of the image
    for i in range(width):
        for j in range(height):
            
            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i
            pos_y = j          
            x = pos_x - width/2
            y = pos_y - height/2
            
            # Calculate the distance from the particular pixel to the center of the object (in pixels)
            r = math.sqrt( x*x + y*y ) + 1 #Rounding correction
        
            #Input ray vector (point in the object plane)
            y_objeto = r*res # Conversion to real world coordinates
            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/so) #This ray enters towards the center of the lens
            elif rayo == 1: #parallel
                alpha_entrada = 0 #This ray enters parallel to the optical axis
            elif rayo == 2: #principal
                alpha_entrada = (math.atan(y_objeto/so))/2 #This ray enters towards the center of the lens
            V_entrada = np.array([n1*alpha_entrada,y_objeto]) 
        
            #Output ray vector calculation
            V_salida = transfmatrix.dot(V_entrada)
        
            #Transversal magnification
            y_imagen = V_salida[1]
            if rayo == 0: #principal
                Mt = (-1)*y_imagen/y_objeto #atan correction
            elif rayo == 1: #parallel
                Mt = y_imagen/y_objeto
            elif rayo == 2: #mid ray
                Mt = y_imagen/y_objeto
    return Mt

#Angle for each ray in the correspondent pixel
def get_alpha(width, height, rayo, n1, so, res, transfmatrix):
    # Iterate over each pixel of the image
    for i in range(width):
        for j in range(height):
            
            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i
            pos_y = j          
            x = pos_x - width/2
            y = pos_y - height/2
            
            # Calculate the distance from the particular pixel to the center of the object (in pixels)
            r = math.sqrt( x*x + y*y ) + 1 #Rounding correction
        
            #Input ray vector (point in the object plane)
            y_objeto = r*res # Conversion to real world coordinates
            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/so) #This ray enters towards the center of the lens
            elif rayo == 1: #parallel
                alpha_entrada = 0 #This ray enters parallel to the optical axis
            elif rayo == 2: #principal
                alpha_entrada = (math.atan(y_objeto/so))/2 #This ray enters towards the center of the lens
            V_entrada = np.array([n1*alpha_entrada,y_objeto]) 
        
            #Output ray vector calculation
            V_salida = transfmatrix.dot(V_entrada)
        
            #Transversal magnification
            alpha = V_salida[0]
    return alpha