import os
import cv2
import numpy as np

def is_bright(img):
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    avg = np.sum(avg_color)/3
    # print(avg)
    return avg > 100 and avg < 120 

def variance_of_laplacian(image):

	return cv2.Laplacian(image, cv2.CV_64F).var()

def is_blurry(image):
    level = variance_of_laplacian(image)
    return level > 120

os.mkdir('tri_lum/')
for root, dirs, files in os.walk("."):
    for name in files:
        if name.endswith(".jpg"):
            img = cv2.imread(os.path.join(root, name))
            if is_bright(img):
                cv2.imwrite("tri_lum/"+name, img)
               
os.mkdir('tri_lum_and_blur/')
for root, dirs, files in os.walk("./tri_lum"):
    for name in files:
        if name.endswith(".jpg"):
            img = cv2.imread(os.path.join(root, name))
            if is_blurry(img):
                cv2.imwrite("tri_lum_and_blur/"+name, img)

def get_mse(original, compressed):
    """
    Compute the MSE of the compressed image and the original image
    
    :param original: The original image
    :param compressed: The compressed image
    :return: the MSE value for the two images.
    """
    mse = np.mean((original - compressed) ** 2)
    return mse