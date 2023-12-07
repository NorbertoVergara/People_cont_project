from ast import Global
import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*
import cvzone
import numpy as np
import os
from ConnectionGSM_GPS import*
import base64

model=YOLO('yolov5s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  
        point = [x, y]
        print(point)
  
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
cap=cv2.VideoCapture('Videos/bus3.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0

tracker=Tracker()
#P
# area1=[(494,289),(505,499),(578,496),(530,292)]
# area2=[(548,290),(600,496),(637,493),(574,288)]

#bus1
#area1=[(400,413),(420,437),(597,286),(567,265)]
#area2=[(428,445),(450,467),(624,319),(598,297)]

#bus3
area1=[(300,460),(300,500),(500,500),(500,460)]
area2= [(428,445),(450,467),(624,319),(598,297)]


going_out={}
going_in={}
counter_salieron=[]
counter_entraron=[]
frames_tomados= {}

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    
    # Incrementar el contador de frames
    count += 1

    # Procesar solo cada tercer frame para reducir la carga computacional
    if count % 1 != 0:
        continue
    
    frame=cv2.resize(frame,(1020,500))
   
    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    
    list= []
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        
        c=class_list[d]
        if 'person' in c :
            list.append([x1,y1,x2,y2])
            
    bbox_idx=tracker.update(list)
    height, width, _ = frame.shape
    for bbox in bbox_idx:
            x3,y3,x4,y4,id=bbox
            # cv2.rectangle(frame, (x3,y3), (x4, y4),(255,0,0),2)
            # cv2.circle(frame,(x3,y4),7,(255,0,255),-1)
            
            result2=cv2.pointPolygonTest(np.array(area2,np.int32),((x4,y4)),False)
            
            if result2>=0:
                going_in[id]=(x3,y4)
            if id in going_in:
                result3=cv2.pointPolygonTest(np.array(area1,np.int32),((x3,y4)),False)
                if result3>=0:
                    cv2.circle(frame,(x3,y4),7,(255,0,255),-1)
                    cv2.rectangle(frame, (x3,y3), (x4, y4),(255,0,0),2)
                    cvzone.putTextRect(frame,f'{id}',(x3,y3),1,1)
                    if counter_entraron.count(id)==0:
                        counter_entraron.append(id)
                    # # Guardar el frame en formato PNG
                    # folder_path = "frames"
                    # if not os.path.exists(folder_path):
                    #     os.makedirs(folder_path)

                    # frame_name = f"frame_{id}.jpeg"
                    # frame_path = os.path.join(folder_path, frame_name)
                    # cv2.imwrite(frame_path, frame)
                    # print(f"Frame guardado en {frame_path}")
                        
                    if id not in frames_tomados:
                    # Marcar el ID como procesado
                        frames_tomados[id] = True
                        # Tu código para convertir el frame a base64 y guardarlo
                        small_frame = cv2.resize(frame, (width // 2, height // 2))
                        _, buffer = cv2.imencode('.jpg', small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                        frame_base64 = base64.b64encode(buffer).decode('utf-8')

                        folder_path = "frames_base64"
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)

                        frame_name = f"frame_{id}.txt"
                        frame_path = os.path.join(folder_path, frame_name)

                        with open(frame_path, 'w') as file:
                            file.write(frame_base64)

                        print(f"Frame en formato base64 guardado en {frame_path}")

            result=cv2.pointPolygonTest(np.array(area1,np.int32),((x4,y4)),False)
            
            # if result>=0:
            #     going_out[id]=(x4,y4)
            # if id in going_out:
            #     result1=cv2.pointPolygonTest(np.array(area2,np.int32),((x4,y4)),False)
            #     if result1>=0:
            #         cv2.circle(frame,(x4,y4),7,(255,0,255),-1)
            #         cv2.rectangle(frame, (x3,y3), (x4, y4),(255,255,255),2)
            #         cvzone.putTextRect(frame,f'{id}',(x3,y3),1,1)
            #         if counter_salieron.count(id)==0:
            #             counter_salieron.append(id)
    
    out_c= len(counter_salieron)
    in_c= len(counter_entraron)
    cvzone.putTextRect(frame,f'Salieron: {out_c}',(50,60),2,2)
    cvzone.putTextRect(frame,f'Entraron: {in_c}',(50,160),2,2)
    cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,255,0),2)
    #cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()



# Direccion mac 
mac = os.popen('getmac /fo csv /nh').read().split(',')[0].strip('"')

import socket
# Obtener el nombre del dispositivo
host_name = socket.gethostname()

import psutil
# Porcentaje de bateria
battery = psutil.sensors_battery()
percent = battery.percent

def connectToSend():
    global _dataFrame
    if configSerialMoule():
        
        if initModule():
          
            if configREDGPRS():
             
                if configGPS():
                   _dataFrame = readGPS()
    
    with open('data.txt','w') as f:
        f.write(f'Nombre del dispositivo: {host_name}\n')
        f.write(f'Total personas que entraron: {in_c}\n')
        f.write(f'total personas que salieron: {out_c}\n')
        f.write(f'mac: {mac}\n')
        f.write(f'{_dataFrame}')
        f.write(f'% bateria: {percent}\n')
        
connectToSend()

print('Data saved to data.txt')

