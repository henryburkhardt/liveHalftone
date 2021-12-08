'''
Live "Halftoning" a Video Input 
Henry Burkhardt 
2021
'''

from PIL import Image, ImageDraw, ImageStat
import cv2
import numpy as np

#Function to scale image by defined scale%
def resizeScale(scale_percent,img):  
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

#Function to scale image by desired number of total pixels
def resizeCirlce(img_input, num_circle):  
    ratio = img_input.shape[1] / img_input.shape[0] #width/height
    width = int(np.sqrt(num_circle*ratio))
    height = int(np.sqrt(num_circle/ratio))
    dim = (width,height)
    resized = cv2.resize(img_input, dim, interpolation = cv2.INTER_AREA) 
    return resized

#Function takes full frame as input and outputs a halftoned frame
def halftone(img_input, num_cicle, scale):
    img = img_input
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = resizeCirlce(img,num_cicle)
    circle_canvas = np.zeros(((img.shape[1]*scale),(img.shape[0]*scale),1),np.uint8)
    circle_canvas.fill(0)
    for x in range(0,img.shape[0],1):
        for y in range(0,img.shape[1],1):
            color = 255 - int(img[x,y])
            diameter = np.sqrt(color/255)
            x_pos = (x * scale) + int(0.5*scale)
            y_pos = (y * scale) + int(0.5*scale)
            diam_calc = diameter * scale
            radius = diam_calc / 2
            cv2.circle(circle_canvas,(x_pos,y_pos),int(radius),255,-1)            
    return cv2.flip(cv2.rotate(circle_canvas,cv2.ROTATE_90_CLOCKWISE),1)

#Empty function to pass to sliders
def nothing(x):
    pass

#Funtion to create input sliders  
def sliderInit():
    cv2.namedWindow('sliders')
    cv2.createTrackbar('cirlces','sliders',1117,20000,nothing)
    cv2.createTrackbar('scale','sliders',100,500,nothing)
    cv2.createTrackbar('qaulity','sliders',58,500,nothing)

#Create background window
#cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
background = np.zeros([512,512,3],dtype=np.uint8)
background.fill(0)
#cv2.imshow('frame',background)

sliderInit()

#Connect video
vid = cv2.VideoCapture(2)
if vid is None or not vid.isOpened():
    vid = cv2.VideoCapture(0)

print("[VIDEO INITIATED]")

while (True):
    ret, frame = vid.read()
    
    #Slider input grab and validation
    circles = cv2.getTrackbarPos('cirlces','sliders')
    scale = cv2.getTrackbarPos('scale','sliders')
    qaulity = cv2.getTrackbarPos('qaulity','sliders')
    #number_circles = 286
    #scale = 24
    #qaulity = 85

    if(circles < 1):
        circles = 2
    if(scale < 1):
        scale = 2
    if (qaulity <1):
        qaulity = 2
    
    #Images to show
    display1 = resizeScale(scale, halftone(frame,circles,qaulity))
    cv2.namedWindow('display1',flags = cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty('display1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('display1', display1)
    #cv2.imshow('display2', display1)
    #cv2.imshow('display3', display1)

    #waitKey escape 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        print("UserQuit")
        break
vid.release()