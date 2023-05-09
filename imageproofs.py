import numpy as np
import math 
import PIL
from PIL import Image
from scipy.interpolate import griddata
from scipy import interpolate
from functions import *
#im = PIL.Image.new(mode = "RGB", size = (200, 200), color = (153, 153, 153))
#im.show()

 #2.606 grados #0.04548328
entry_angles = np.linspace(0, 0.04548328, 20)
                for alpha in entry_angles:
                    ray_ie = np.array([y_object, alpha]).reshape(2, 1)
                    d = dist_eyepice_sensor
                    ray_is = np.array([[1, si],[0, 1]]) @ sensor.transference_matrix @ np.array([[1, d],[0, 1]]) @ self.ABCD_matrix @ np.array([[1, n_so/so],[0, 1]]) @ ray_ie

                    y_image = ray_is[0]
                    Mt = y_image / y_object


                    x_prime = Mt*x
                    y_prime = Mt*y

                    pos_x_prime = int(x_prime + width_output/2)
                    pos_y_prime = int(y_prime + height_output/2)

                    if pos_y_prime <= 0 or pos_y_prime >= height_output:   
                        continue 
                    elif pos_x_prime <= 0 or pos_x_prime >= width_output:
            	        continue
                    
                    rays_lost = 0
                    try:
                        new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0])/2
                    except:
                        rays_lost += 1

                    pix_fin = ( int(new_gray), int(new_gray), int(new_gray) )        
                    pixels[pos_x_prime, pos_y_prime] = pix_fin


        print(rays_lost)

        image.save('output/moon_out.png', format='PNG')

        return pixels, width_output, height_output
