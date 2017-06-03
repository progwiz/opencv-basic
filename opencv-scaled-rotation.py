import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

#find location of a particular point after rotation
def rotate_point(point,angle,pivot,scale):
    cos=scale*math.cos(angle)
    sin=scale*math.sin(angle)
    x=(point[0]-pivot[0])*cos-(point[1]-pivot[1])*sin
    y=(point[1]-pivot[1])*cos+(point[0]-pivot[0])*sin
    return int(x+pivot[0]),int(y+pivot[1])


#rotate an image by the angle specified in degrees about a pivot point
def rotate(image, angle, scale=1.0, pivot=(0,0), reshape=True):
    (h, w) = image.shape[:2]
    angle_rad=angle*math.pi/180
    # if reshape==True, borders are extended to retain all data from input image
    if reshape:
        cos=scale*math.cos(angle_rad)
        sin=scale*math.sin(angle_rad)
        
        #find new locations of corner points of the image
        x1,y1=rotate_point([h,0],-angle_rad,pivot,scale)
        x2,y2=rotate_point([0,w],-angle_rad,pivot,scale)
        x3,y3=rotate_point([h,w],-angle_rad,pivot,scale)
        x4,y4=rotate_point([0,0],-angle_rad,pivot,scale)
        x=[x1,x2,x3,x4]
        y=[y1,y2,y3,y4]
        x_min=min(x)
        x_max=max(x)
        y_min=min(y)
        y_max=max(y)
        M = np.array([[cos,-sin,(pivot[1]*(1-cos)+pivot[0]*sin-y_min)],[sin,cos,(pivot[0]*(1-cos)-pivot[1]*sin-x_min)]])
        nW=y_max-y_min
        nH=x_max-x_min
    else: 
        x_min=0
        y_min=0
        nW=w
        nH=h
        M = cv2.getRotationMatrix2D(pivot, -angle, 1.0)
    return cv2.warpAffine(image, M, (nW, nH))



# test code
"""
img=cv2.imread("sample.jpg",cv2.IMREAD_COLOR)
fig=plt.figure(0)
fig.add_subplot(4,1,1)
plt.imshow(img)
fig.add_subplot(4,1,2)
plt.imshow(rotate(img,15),'gray')
fig.add_subplot(4,1,3)
plt.imshow(rotate(img,15,reshape=False),'gray')
fig.add_subplot(4,1,4)
plt.imshow(rotate(img,15,pivot=(img.shape[0]//2,img.shape[1]//2)),'gray')
"""