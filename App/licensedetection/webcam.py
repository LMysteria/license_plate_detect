from PIL import Image
import cv2
import torch
import math 
import function.utils_rotate as utils_rotate
import os
import time
import argparse
import function.helper as helper
import warnings
import requests
from datetime import timedelta
warnings.simplefilter(action='ignore', category=FutureWarning)

#Login information
username:str = "Mystic"
password:str = "123asdASD!"
backendcontext:str = "http://localhost:8000"

#Parking Check in, Check out info
isCheckIn:bool = True
parkingareaid:int = 1

#User tags
userid:int = 1

def webcam():
    # load model
    yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='./App/licensedetection/model/LP_detector_nano_61.pt', force_reload=True, source='local')
    yolo_license_plate = torch.hub.load('yolov5', 'custom', path='./App/licensedetection/model/LP_ocr_nano_62.pt', force_reload=True, source='local')
    yolo_license_plate.conf = 0.60

    prev_frame_time = 0
    new_frame_time = 0

    vid = cv2.VideoCapture(0)
    # vid = cv2.VideoCapture("1.mp4")
    
    vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        
    pre_lp = ""
    start: time = time.time()
    isSend: bool = False
    global isCheckIn

    while(True):
        ret, frame = vid.read()
        
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
                form = {"parkingareaid":parkingareaid, "userid":userid, "license":lp}
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
                print("Receive response in: {}s".format(time.time()-start))
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord("o"):
            pre_lp=""
            isCheckIn = False
            print("Switch to check out")
        if cv2.waitKey(1) & 0xFF == ord("i"):
            pre_lp=""
            isCheckIn = True
            print("Switch to check in")

    vid.release()
    cv2.destroyAllWindows()

#Login request
login_form = {"username":username, "password":password}
response = requests.post(backendcontext+"/login", data=login_form)
if response.status_code == 200:
    data = response.json()
    token: str = data["access_token"]
    admincheck = requests.get(backendcontext+"/admin/",headers={f"Authorization": "Bearer "+token})
    if admincheck.status_code == 200:
        print("Login Success!")
        webcam()
    else: print(f"Login failed: {admincheck.status_code}")
else:
    print(f"Login failed: {response.status_code}")