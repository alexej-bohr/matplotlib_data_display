'''
Created on 05.11.2019

@author: Alexej.Bohr
'''

import sys
import ctypes
from ctypes import Structure
import platform
if (platform.system() == 'Windows'):
    serialport = 'COM8'
elif (platform.system() == 'Linux'):
    serialport = '/dev/ttyUSB0'


''' Example Uart print
b'\rS\x00C\x00P\x00-\x00U\x00H\x00P\x00:\x00 NumDet:19\n'
b'\rSCP-UHP:   0;  42.268;  0.4;  0.0\n'
b'\rSCP-UHP:   1;  80.780;  0.4;  0.0\n'
'''



import serial

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib import style,  transforms
import numpy as np



def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

ser = serial.Serial(serialport,120000)
print(ser.name)
counter = 0 
run = True

detectionList = []
startDetectionList = False
currentDetectionsCounter = 0

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability

data_started = False

#while run:
def animate(i, xs, ys):

    global number_detections
    global currentDetectionsCounter
    global det_num
    global data_started
    
    s = ser.readline()
    if (not data_started):
        print(s)

    if (b"NumDet:" in s):
        sub_strings = s.split(b"NumDet:")
        number_detections = int(sub_strings[1])
        global startDetectionList
        startDetectionList = True
        currentDetectionsCounter = 0
        ys.clear()
        xs.clear()
        data_started = True


    elif (startDetectionList and number_detections>0 ):
        sub_strings = s.split(b"UHP:")
        if (len(sub_strings)==2):
            sub_strings = sub_strings[1]
            sub_strings = sub_strings.split(b";")
            if (len(sub_strings)==4):
                try:
                    det_num = int(sub_strings[0])
                except: 
                    # skip this scan
                    det_num = number_detections
                try: 
                    det_range = float(sub_strings[1])
                except:
                    det_range = 0.0
                try:
                    det_azimuth = float(sub_strings[2])
                except:
                    det_azimuth =0.0
                #det_elevation = float(sub_strings[3])

                x, y = pol2cart(det_range, det_azimuth)
                xs.append(x)
                ys.append(y)


        

        if (det_num == (number_detections-1) ):
            startDetectionList = False
                # Draw x and y lists
            global ax
            ax.clear()
           # first of all, the base transformation of the data points is needed
            base = plt.gca().transData
            plt.axis([-5, 5, 0, 10]) #Use for arbitrary number of trial
            rot = transforms.Affine2D().rotate_deg(90)
            ax.plot(xs, ys, "x", transform= rot + base)
            #ax.plot(xs, ys,"x")

    
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
plt.show()
        






