#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
cap = cv2.VideoCapture("q2.mp4")

w = 1000
h = 600

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    frame1 = cv2.resize(frame, (w, h))
    
    img_hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

    orig = frame1.copy()
    
    #Segmentando Cartas vermelhas
    
    image_lower_Vermelha = np.array([0, 150, 50])  
    image_upper_Vermelha = np.array([255, 255, 255])
    mask_hsvVermelha = cv2.inRange(img_hsv, image_lower_Vermelha, image_upper_Vermelha)
    
    CartaSeparadoVermelha = cv2.cvtColor(mask_hsvVermelha, cv2.COLOR_BGR2RGB)
    
    grayVermelha = cv2.cvtColor(CartaSeparadoVermelha, cv2.COLOR_BGR2GRAY)
    edgedVermelha = cv2.Canny(grayVermelha, 50, 150)
    dilateVermelha = cv2.dilate(edgedVermelha, None, iterations=22)
    erodeVermelha = cv2.erode(dilateVermelha, None, iterations=2)
    
    cntsVermelha, _ = cv2.findContours(erodeVermelha.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    (cntsVermelha, boundingBoxes) = zip(*sorted(zip(cntsVermelha, [cv2.boundingRect(c) for c in cntsVermelha]), key=lambda b: b[1][0], reverse=False))
    
    
    numeroCartaVermelha = 0
    
    for c in cntsVermelha:
  # se o contorno não é suficientemente grande, ignorá-lo
        if cv2.contourArea(c) > 10000:
            area = cv2.contourArea(c)
            boxVermelha = cv2.minAreaRect(c)
            boxVermelha = cv2.boxPoints(boxVermelha) 
            boxVermelha = np.array(boxVermelha, dtype="int")
            
            if area > 24000 and area < 24600:
                continue
            else:
                #cv2.drawContours(orig, [boxVermelha.astype("int")], -3, (0, 255, 0), 2)
                numeroCartaVermelha = numeroCartaVermelha + 1
    
    
    
    #Segmentando Cartas Pretas
    
    image_lower_Preta = np.array([0, 0, 0])  
    image_upper_Preta = np.array([200, 100, 100])
    mask_hsvPreta = cv2.inRange(img_hsv, image_lower_Preta, image_upper_Preta)
    
    CartaSeparadoPreta = cv2.cvtColor(mask_hsvPreta, cv2.COLOR_BGR2RGB)
    grayPreta = cv2.cvtColor(CartaSeparadoPreta, cv2.COLOR_BGR2GRAY)
    edgedPreta = cv2.Canny(grayPreta, 50, 150)
    dilatePreta = cv2.dilate(edgedPreta, None, iterations=9)
    erodePreta = cv2.erode(dilatePreta, None, iterations=1)
   

    cntsPreta, _ = cv2.findContours(erodePreta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    
    orig = frame1.copy()
    
    numeroCartaPreta = 0
    
    if cntsPreta == ():
        continue
    else:
        (cntsPreta, boundingBoxes) = zip(*sorted(zip(cntsPreta, [cv2.boundingRect(c) for c in cntsPreta]), key=lambda b: b[1][0], reverse=False))
        for c in cntsPreta:
  # se o contorno não é suficientemente grande, ignorá-lo
            if cv2.contourArea(c) >= 17000:
                boxPreta = cv2.minAreaRect(c)
                boxPreta = cv2.boxPoints(boxPreta) 
                boxPreta = np.array(boxPreta, dtype="int")
                #cv2.drawContours(orig, [boxPreta.astype("int")], -1, (217, 35, 217), 2)
                numeroCartaPreta = numeroCartaPreta + 1
                


    # Exibe resultado
    origem_areaPreta = (250,590)
    font_area = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(orig, str("Pretas: {}").format(numeroCartaPreta), origem_areaPreta, font_area,1,(0, 0, 0),2,cv2.LINE_AA)

    origem_areaPreta = (10,590)
    font_area = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(orig, str("Vermelhas: {}").format(numeroCartaVermelha), origem_areaPreta, font_area,1,(0, 0, 0),2,cv2.LINE_AA)

    
    cv2.imshow("Saida Visual", orig)
    

    # Wait for key 'ESC' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

# That's how you exit
cap.release()
cv2.destroyAllWindows()
