from skimage.metrics import structural_similarity
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageFilter
from PIL.ExifTags import TAGS

#Read images
img1 = Image.open("eiffel.jpg", 'r') #Read original image1
img2 = Image.open('eiffelnointer_output.png', 'r') #Read image1 processed (magnified) non interpolated
img3 = Image.open('eiffel_output.png', 'r') #Read image 1 processed (magnified) interpolated
img4 = Image.open('moon.png', 'r')  #Read original image 2
img5 = Image.open('moonnointer_output.png', 'r')  #Read image 2 (magnified) non interpolated
img6 = Image.open('moon_output.png', 'r')  #Read image 2 (magnified) interpolated

#Obtain metadata of the images
w1, h1 = img1.size 
w2, h2 = img2.size
w4, h4 = img4.size
w5, h5 = img5.size

#Verifying magnification of the original image
height_magnification1 = (h2/h1)
#print("height magnification", height_magnification1)
width_magnification1 = (w2/w1)
#print("width magnification", width_magnification1)
height_magnification2 = (h5/h4)
#print("height magnification", height_magnification2)
width_magnification2 = (w5/w4)
#print("width magnification", width_magnification2)

#Compute colors count for each image
colors_img1=Image.Image.getcolors(img1)         #Colors of original image 1
colors_img3=Image.Image.getcolors(img3)         #Colors of image 1 magnified and interpolated

#print(colors_img1)
print(colors_img1)
print(colors_img3)


def counter (pixels, width_o, height_o, channels):
    arry = np.zeros((width_o, height_o))
    for i in range(width_o):
        for j in range(height_o):
            arry[i,j] = pixels[i,j][1]
    return arry

img1_1 = Image.open("eiffel_output.png", 'r') #Read original image1
pixels = img1_1.load()
#print(pixels)
#print(counter(pixels, w1, h1, 2))

#Show processed images (0 if eiffel, 1 if moon)
show = 0
#Display the two images in one figure
if show==0:
    fig1 = plt.figure(figsize=(100, 100))
    rows = 1
    columns = 2
    fig1.add_subplot(rows, columns, 1)
    plt.imshow(img1, cmap='gray')
    plt.axis('on')
    plt.title("Original Image")
    fig1.add_subplot(rows, columns, 2)
    plt.imshow(img2)
    plt.axis('on')
    plt.title("Processed Image" )
    plt.show()

    fig2 = plt.figure(figsize=(100, 100))
    rows = 1
    columns = 2
    fig2.add_subplot(rows, columns, 1)
    plt.imshow(img1, cmap='gray')
    plt.axis('on')
    plt.title("Original Image")
    fig2.add_subplot(rows, columns, 2)
    plt.imshow(img3)
    plt.axis('on')
    plt.title("Processed and Interpolated Image" )
    plt.show()
elif show==1:
    fig1 = plt.figure(figsize=(100, 100))
    rows = 1
    columns = 2
    fig1.add_subplot(rows, columns, 1)
    plt.imshow(img4, cmap='gray')
    plt.axis('on')
    plt.title("Original Image")
    fig1.add_subplot(rows, columns, 2)
    plt.imshow(img5)
    plt.axis('on')
    plt.title("Processed Image" )
    plt.show()

    fig2 = plt.figure(figsize=(100, 100))
    rows = 1
    columns = 2
    fig2.add_subplot(rows, columns, 1)
    plt.imshow(img4, cmap='gray')
    plt.axis('on')
    plt.title("Original Image")
    fig2.add_subplot(rows, columns, 2)
    plt.imshow(img6)
    plt.axis('on')
    plt.title("Processed and Interpolated Image" )
    plt.show()