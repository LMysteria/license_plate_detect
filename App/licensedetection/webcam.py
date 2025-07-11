from PIL import Image
import cv2
import torch
import math 
from .function import utils_rotate
import os
import time
import argparse
from .function import helper
import warnings
import requests
import asyncio
import base64
from datetime import timedelta
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
warnings.simplefilter(action='ignore', category=FutureWarning)

#User tags
userid:int = 1
# load model
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='./App/licensedetection/model/LP_detector_nano_61.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='./App/licensedetection/model/LP_ocr_nano_62.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.60

async def webcam(parkingareaid:int, isCheckIn:bool, camera_num:int, websocket:WebSocket):
    
    global yolo_LP_detect
    global yolo_license_plate

    prev_frame_time = 0
    new_frame_time = 0

    vid = cv2.VideoCapture(camera_num)
    # vid = cv2.VideoCapture("1.mp4")
    
    vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        
    pre_lp = ""
    start: time = time.time()
    isSend: bool = False
    try:
        while(True):
            ret, frame = vid.read()
            if not ret:
                print("frame not capture")
                continue
            
            plates = yolo_LP_detect(frame, size=640)
            list_plates = plates.pandas().xyxy[0].values.tolist()
            list_read_plates = set()
            for plate in list_plates:
                flag = 0
                x = int(plate[0]) # xmin
                y = int(plate[1]) # ymin
                w = int(plate[2] - plate[0]) # xmax - xmin
                h = int(plate[3] - plate[1]) # ymax - ymin  
                crop_img = frame[y:y+h, x:x+w]
                cv2.rectangle(frame, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
                cv2.imwrite("crop.jpg", crop_img)
                rc_image = cv2.imread("crop.jpg")
                lp = ""
                for cc in range(0,2):
                    for ct in range(0,2):
                        lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                        if lp != "unknown":
                            list_read_plates.add(lp)
                            cv2.putText(frame, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                            flag = 1
                            break
                    if flag == 1:
                        break
                if((lp not in pre_lp) & (lp != "unknown")):
                    pre_lp = lp
                    start = time.time()
                    isSend = False
                    print(pre_lp)
                elif((lp == pre_lp) & ((time.time() - start) >= 2) & (isSend == False)):
                    isSend = True
                    print("Send detected license {}".format(pre_lp))
                    cv2.imwrite("temp.jpg",frame)
                    start = time.time()
                    """form = {"parkingareaid":parkingareaid, "userid":userid, "license":lp}
                    images = {'img': open('temp.jpg','rb')}
                    print(form)
                    if(isCheckIn):
                        response = requests.post(f"{backendcontext}/admin/parkinglot/parkingarea/parkingdata/entry",data=form, headers={f"Authorization": "Bearer "+token}, files=images)
                    else:
                        response = requests.post(f"{backendcontext}/admin/parkinglot/parkingarea/parkingdata/exit",data=form, headers={f"Authorization": "Bearer "+token}, files=images)
                    if response.status_code == 200:
                        print("Record successful")
                        print(response.json())
                    else:
                        print("Record Failed")
                        print(response.json())
                    print("Receive response in: {}s".format(time.time()-start))"""
            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Frame failed to encode")
                continue
            
            frame_bytes = buffer.tobytes()
            try:
                if websocket.client_state != WebSocketState.CONNECTED:
                    print("Socket no longer connected")
                    break
                
                await websocket.send_bytes(frame_bytes)
                await asyncio.sleep(0.03)
            
            except RuntimeError as e:
                print("Socket send failed", e)
                break
            
            except WebSocketDisconnect:
                print("Websocket Disconnected")
                break
            
    except Exception as e:
        print("Unexpected error during streaming:", e)
    
    finally:
        print("Release camera and clean up")
        vid.release()
