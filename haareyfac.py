'''
  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.
  By downloading, copying, installing or using the software you agree to this license.
  If you do not agree to this license, do not download, install,
  copy or use the software.
                        Intel License Agreement
                For Open Source Computer Vision Library
 Copyright (C) 2000, Intel Corporation, all rights reserved.
 Third party copyrights are property of their respective owners.
 Redistribution and use in source and binary forms, with or without modification,
 are permitted provided that the following conditions are met:
   * Redistribution's of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
   * Redistribution's in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.
   * The name of Intel Corporation may not be used to endorse or promote products
     derived from this software without specific prior written permission.
 This software is provided by the copyright holders and contributors "as is" and
 any express or implied warranties, including, but not limited to, the implied
 warranties of merchantability and fitness for a particular purpose are disclaimed.
 In no event shall the Intel Corporation or contributors be liable for any direct,
 indirect, incidental, special, exemplary, or consequential damages
 (including, but not limited to, procurement of substitute goods or services;
 loss of use, data, or profits; or business interruption) however caused
 and on any theory of liability, whether in contract, strict liability,
 or tort (including negligence or otherwise) arising in any way out of
 the use of this software, even if advised of the possibility of such damage.
'''

import numpy as np
import cv2
import serial
import time

#multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
1
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
PORT = "COM3"
BAUD_RATE = 9600 	#This depends on your microprocessor's clock frequency
ser = serial.Serial(PORT, BAUD_RATE)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0) #0 for the webcam, 1 for the primary camera and so on
flag = 100
while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) #The figures 1.3 and 5 depend on the size of the image and the likelihood of finding a face in the image

        if(len(faces)!=0):
                ser.write("7")
                #ser.write("5")


        for(x, y, w, h) in faces: #x, y Cartesian Co-ordinates, width and height
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) #Drawing a rectangle

                #roi_gray = gray[y:y+h, x:x+w] #Cropping the Gray Region Of Interest, always Y:X
                #roi_color = img[y:y+h, x:x+w]
                #eyes = eye_cascade.detectMultiScale(roi_gray) #Relying on default values

                #for(ex, ey, ew, eh) in eyes:
                #cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        #ser.write("5")
        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff

        if k == 27:
                break

#ser.close()

cap.release()
cv2.destroyAllWindows()
