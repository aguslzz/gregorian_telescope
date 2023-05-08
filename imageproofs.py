import numpy as np
import math 
import PIL
from PIL import Image
from scipy.interpolate import griddata

from scipy import interpolate
im = PIL.Image.new(mode = "RGB", size = (200, 200), color = (153, 153, 153))
im.show()