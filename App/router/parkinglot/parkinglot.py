from fastapi import APIRouter, UploadFile, Form, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.responses import StreamingResponse
from typing import Annotated
from . import parkinglotcrud, parkinglotutil
from ... import util
from ...licensedetection.webcam import webcam
from ...auth import authcontroller
import time

parkinglotrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])
ParkinglotUserrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])

@parkinglotrouter.get("/parkingarea/parkingdata")
def get_parkingdata_detail(parkingdataid:int):
    start = time.time()
    response = parkinglotcrud.get_parkingdata_by_id(id=parkingdataid)
    util.time_message("get parking data with id {}".format(parkingdataid), starttime=start)
    return response

@ParkinglotUserrouter.websocket("/parkingarea/camera")
async def get_parkingarea_camera(parkingareaid:int, ischeckin:bool, camera_num:int, websocket: WebSocket):
    print("Attempt connect")
    await websocket.accept()
    print("Websocket connected")
    try:
        await webcam(parkingareaid=parkingareaid, isCheckIn=ischeckin, camera_num=camera_num, websocket=websocket)
    except WebSocketDisconnect:
        print("client disconnected")
    except Exception as e:
        raise e
    finally:
        await websocket.close()
        print("Websocket close")

@parkinglotrouter.post("/create")
def create_parkinglot(name:Annotated[str, Form()], address:Annotated[str, Form()], lat:Annotated[float, Form()], lng:Annotated[float, Form()],
                      dayfeemotorbike:Annotated[float, Form()], nightfeemotorbike:Annotated[float, Form()], carfee:Annotated[float, Form()],
                      img: Annotated[UploadFile, None] = None):
    start = time.time()
    response = parkinglotutil.create_parkinglot(name=name, address=address, lat=lat, lng=lng, dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee, img=img)
    util.time_message(f"create parking lot successfully",start)
    return response

@parkinglotrouter.post("/parkingarea/create")
def create_parkinglot(area:Annotated[str, Form()], maxspace:Annotated[int, Form()], remainingspace:Annotated[int, Form()], 
                      parkinglotid: Annotated[int, Form()], iscar: Annotated[bool, Form()],
                      img: Annotated[UploadFile, None] = None):
    start = time.time()
    response = parkinglotutil.create_parkingarea(area=area, maxspace=maxspace, remainingspace=remainingspace, parkinglotid=parkinglotid, iscar=iscar, img=img)
    util.time_message(f"create parking area in parking lotid {parkinglotid} successfully",start)
    return response

@parkinglotrouter.post("/parkingarea/parkingdata/entry")
def parking_entry(img: UploadFile, parkingareaid: Annotated[int, Form()], userid: Annotated[int, Form()], license: Annotated[str, Form()]):
    start = time.time()
    response = parkinglotutil.parking_entry(img=img, parkingareaid=parkingareaid, userid=userid, detected=license)
    util.time_message(f"parkingdata for userid {userid} entry parking areaid {parkingareaid} successfully",start)
    return response

@parkinglotrouter.post("/parkingarea/parkingdata/exit")
def parking_exit(img: UploadFile, parkingareaid: Annotated[int, Form()], userid: Annotated[int, Form()], license: Annotated[str, Form()]):
    start = time.time()
    response = parkinglotutil.parking_exit(img=img, parkingareaid=parkingareaid, userid=userid, detected=license)
    util.time_message(f"parkingdata for userid {userid} exit parking areaid {parkingareaid} successfully",start)
    return response

@parkinglotrouter.post("/update")
def update_parkingarea_image(parkinglotid: Annotated[int, Form()], name:Annotated[str, Form()], address:Annotated[str, Form()], lat:Annotated[float, Form()], lng:Annotated[float, Form()],
                             dayfeemotorbike:Annotated[float, Form()], nightfeemotorbike:Annotated[float, Form()], carfee:Annotated[float, Form()], 
                             img: Annotated[UploadFile, None] = None):
    start = time.time()
    response = parkinglotutil.update_parkinglot(img=img, parkinglotid=parkinglotid, name=name, address=address, lat=lat, lng=lng,
                                            dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee)
    util.time_message(f"update parkinglotid {parkinglotid} detail successfully",start)
    return response

@parkinglotrouter.post("/parkingarea/update")
def update_parkingarea_image(parkingareaid: Annotated[int, Form()], area:Annotated[str, Form()], maxspace:Annotated[int, Form()], remainingspace:Annotated[int, Form()], 
                      iscar: Annotated[bool, Form()], img: Annotated[UploadFile, None] = None):
    start = time.time()
    response = parkinglotutil.update_parkingarea(img=img, parkingareaid=parkingareaid, area=area, maxspace=maxspace, remainingspace=remainingspace, iscar=iscar)
    util.time_message(f"update parkingareaid {parkingareaid} detail successfully",start)
    return response

@parkinglotrouter.post("/parkingarea/parkingdata/manualcheck/create")
def parkingdata_manualcheck(cid_img: UploadFile, cavet_img: UploadFile, parkingdataid: Annotated[int, Form()]):
    start = time.time()
    response = parkinglotutil.manual_check(cid_img=cid_img, cavet_img=cavet_img, parkingdataid=parkingdataid)
    util.time_message(f"create manual check form for parkingdataid {parkingdataid} successfully",start)
    return response

@ParkinglotUserrouter.get("")
def get_parkinglot_detail(parkinglotid:int):
    start = time.time()
    response = parkinglotcrud.get_parkinglot_by_id(id=parkinglotid)
    util.time_message(f"get parking lot with id {parkinglotid}",start)
    return response

@ParkinglotUserrouter.get("/list")
def get_parkinglot_list(search: str = "", skip: int = 0, limit: int = 10):
    start = time.time()
    response = parkinglotutil.parkinglotlist(search=search, skip=skip,limit=limit)
    util.time_message(f"search parking lot list",start)
    return response

@ParkinglotUserrouter.get("/parkingarea")
def get_parkingarea_detail(parkingareaid:int):
    start = time.time()
    response = parkinglotcrud.get_parkingarea_by_id(id=parkingareaid)
    util.time_message(f"get parking area with id {parkingareaid}",start)
    return response

@ParkinglotUserrouter.get("/parkingarea/list")
def get_parkinglot_list(parkinglotid: int):
    start = time.time()
    response = parkinglotcrud.get_parkingarea_by_parkinglotid(parkinglotid=parkinglotid)
    util.time_message(f"get parking area list in parking lotid {parkinglotid}",start)
    return response