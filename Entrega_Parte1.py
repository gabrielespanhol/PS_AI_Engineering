import cv2
import numpy as np
cap = cv2.VideoCapture("q1A.mp4")


while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
     
    # isolando forma geométrica vermelha   
    image_lower_vermelha = np.array([0, 215, 70])  
    image_upper_vermelha = np.array([255, 255, 255])
    mask_hsv_vermelha = cv2.inRange(img_hsv, image_lower_vermelha, image_upper_vermelha)

    edged_vermelha = cv2.Canny(mask_hsv_vermelha, 50, 150)
    dilate_vermelha = cv2.dilate(edged_vermelha, None, iterations=2)
    erode_vermelha = cv2.erode(dilate_vermelha, None, iterations=1)
    
    # contorno camada vermelha
    cnts_vermelha, _ = cv2.findContours(erode_vermelha.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    (cnts_vermelha, boundingBoxes) = zip(*sorted(zip(cnts_vermelha, [cv2.boundingRect(c) for c in cnts_vermelha]), key=lambda b: b[1][0], reverse=False))
    
    
    
    # isolando forma geométrica azul
    image_lower_azul = np.array([100, 150, 100])  
    image_upper_azul = np.array([150, 200, 250]) 
    mask_hsv_azul = cv2.inRange(img_hsv, image_lower_azul, image_upper_azul)
    
    edged_azul = cv2.Canny(mask_hsv_azul, 50, 150)
    dilate_azul = cv2.dilate(edged_azul, None, iterations=2)
    erode_azul = cv2.erode(dilate_azul, None, iterations=1)
    
    # contorno camada azul
    cnts_azul, _ = cv2.findContours(erode_azul.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    (cnts_azul, boundingBoxes) = zip(*sorted(zip(cnts_azul, [cv2.boundingRect(c) for c in cnts_azul]), key=lambda b: b[1][0], reverse=False))

    
    
    orig = frame.copy()

    c_v = cnts_vermelha[0] 
    c_a = cnts_azul[0]

    box_vermelha = cv2.minAreaRect(c_v)
    box_vermelha = cv2.boxPoints(box_vermelha) 
    
    box_azul = cv2.minAreaRect(c_a)
    box_azul = cv2.boxPoints(box_azul) 
    
    
        
    # verificando qual contono tem a maior área
    if cv2.contourArea(c_v) > cv2.contourArea(c_a):
        
        box_vermelha = np.array(box_vermelha, dtype="int")
        cv2.drawContours(orig, [box_vermelha.astype("int")], -1, (0, 255, 0), 2)
        
    elif cv2.contourArea(c_a) > cv2.contourArea(c_v): 

        box_azul = np.array(box_azul, dtype="int")
        cv2.drawContours(orig, [box_azul.astype("int")], -1, (0, 255, 0), 2)
    
        
    if ((box_azul[2][1] > box_vermelha[0][1]) or (box_azul[0][1] >= box_vermelha[2][1]) or (((box_azul[0][1]/2) >= box_vermelha[2][1]))) and (box_azul[2][0] > box_vermelha[0][0]):
        origem_area = (650,100)
        font_area = cv2.FONT_HERSHEY_SIMPLEX
        
        
        if box_vermelha[1][0] and box_vermelha[2][0] < box_azul[0][0] and box_azul[3][0]: 
    
            origem_area = (650,100)
            font_area = cv2.FONT_HERSHEY_SIMPLEX
    
            cv2.putText(orig, str("PASSOU DA BARREIRA"), origem_area, font_area,2,(20, 184, 184),2,cv2.LINE_AA)
        else:
            
            cv2.putText(orig, str("COLISAO DETECTADA"), origem_area, font_area,2,(20, 184, 184),2,cv2.LINE_AA)
            
    if box_vermelha[1][0] and box_vermelha[2][0] < box_azul[0][0] and box_azul[3][0]: 
    
            origem_area = (650,100)
            font_area = cv2.FONT_HERSHEY_SIMPLEX
    
            cv2.putText(orig, str("PASSOU DA BARREIRA"), origem_area, font_area,2,(20, 184, 184),2,cv2.LINE_AA)
    

    # Exibe resultado
    cv2.imshow("Feed", orig)

    # Wait for key 'ESC' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

# That's how you exit
cap.release()
cv2.destroyAllWindows()