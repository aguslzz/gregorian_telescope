from skimage.metrics import structural_similarity
import cv2
from matplotlib import pyplot as plt
import numpy
from PIL import Image
from PIL.ExifTags import TAGS

#Read images
img1 = Image.open("eiffel.jpg", 'r') #Read original image1
#gray_img1 = img1.convert("L")
img2 = Image.open('eiffel_output.png') #Read image1 processed (magnified)
img3 = Image.open('moon.png') #Read original image2
img4 = Image.open('moon_output.png')  #Read image2 processed (magnified)

#Obtain metadata of the images
h1 = img1.height 
w1 = img1.width
h2 = img2.height
w2 = img2.width
h3 = img3.height
w3 = img3.width
h4 = img4.height
w4 = img4.width

#Verifying magnification of the original image
height_magnification1 = (h2/h1)
print("height magnification", height_magnification1)
width_magnification1 = (w2/w1)
print("width magnification", width_magnification1)
height_magnification2 = (h4/h3)
print("height magnification", height_magnification2)
width_magnification2 = (w4/w3)
print("width magnification", width_magnification2)

#Compute SSIM between two images
#(score, diff) = structural_similarity(img1, img2, full=True)
#print("The structural similarity index measure (SSIM) is:", score)

#Display the two images in one figure
fig1 = plt.figure(figsize=(100, 100))
rows = 1
columns = 2
fig1.add_subplot(rows, columns, 1)
plt.imshow(img1, cmap='gray')
plt.axis('off')
plt.title("Original Image")
fig1.add_subplot(rows, columns, 2)
plt.imshow(img2)
plt.axis('off')
plt.title("Processed Image" )
plt.show()

fig2 = plt.figure(figsize=(100, 100))
rows = 1
columns = 2
fig2.add_subplot(rows, columns, 1)
plt.imshow(img3, cmap='gray')
plt.axis('off')
plt.title("Original Image")
fig2.add_subplot(rows, columns, 2)
plt.imshow(img4)
plt.axis('off')
plt.title("Processed Image" )
plt.show()