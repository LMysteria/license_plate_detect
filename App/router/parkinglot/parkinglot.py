from fastapi import APIRouter, UploadFile, Form, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.responses import StreamingResponse
from typing import Annotated
from . import parkinglotcrud, parkinglotutil
from ... import util
from ...licensedetection.webcam import webcam
from ...auth import authcontroller
from ..user import usercrud
from ...database.crud import get_image_byID
from ...schema.data import ParkingData
from datetime import datetime
import time

parkinglotrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])
ParkinglotUserrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])

@parkinglotrouter.get("/parkingarea/parkingdata")
def get_parkingdata_detail(parkingdataid:int):
    start = time.time()
    response = parkinglotcrud.get_parkingdata_by_id(id=parkingdataid)
    util.time_message("get parking data with id {}".format(parkingdataid), starttime=start)
    return response

@parkinglotrouter.get("/parkingarea/parkingdata/last")
def get_parkingdata_detail(parkingareaid:int, userid:Annotated[int, None] = None, licenseplate:Annotated[str,None]= None):
    start = time.time()
    if(userid):
        response = parkinglotcrud.get_last_parkingdata_by_userid(parkingareaid=parkingareaid, userid=userid)
        util.time_message("get parking data with userid {}".format(userid), starttime=start)
    else:
        response = parkinglotcrud.get_last_parkingdata_by_licensenumber(parkingareaid=parkingareaid, licensenumber=licenseplate)
        util.time_message("get parking data with license {}".format(licenseplate), starttime=start)
    transaction = usercrud.get_transaction_by_parkingid(parkingdataid=response.id)
    if(response.exit_time):
        return ParkingData(id=response.id, userid=transaction.userid, license=response.license, 
                       entry_time=datetime.strftime(response.entry_time,"%X, %x"), entry_path=get_image_byID(response.entry_img).path, 
                       exit_time=datetime.strftime(response.exit_time,"%X, %x"), exit_path=get_image_byID(response.exit_img).path)
    return ParkingData(id=response.id, userid=transaction.userid, license=response.license, 
                       entry_time=datetime.strftime(response.entry_time,"%X, %x"), entry_path=get_image_byID(response.entry_img).path)

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
                      dayfeemotorbike:Annotated[float, Form()]=0, nightfeemotorbike:Annotated[float, Form()]=0, carfee:Annotated[float, Form()]=0,
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

@ParkinglotUserrouter.post("/parkingarea/parkingdata/entry")
def parking_entry(img: UploadFile, parkingareaid: Annotated[int, Form()], userid: Annotated[int, Form()], license: Annotated[str, Form()], token: Annotated[str, Form()]):
    authcontroller.check_ADMIN_KEY(token=token)
    start = time.time()
    response = parkinglotutil.parking_entry(img=img, parkingareaid=parkingareaid, userid=userid, detected=license)
    util.time_message(f"parkingdata for userid {userid} entry parking areaid {parkingareaid} successfully",start)
    return response

@ParkinglotUserrouter.post("/parkingarea/parkingdata/exit")
def parking_exit(img: UploadFile, parkingareaid: Annotated[int, Form()], userid: Annotated[int, Form()], license: Annotated[str, Form()], token: Annotated[str, Form()]):
    authcontroller.check_ADMIN_KEY(token=token)
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
def get_parkinglot_list(lat:Annotated[float, None]= None, lng:Annotated[float, None]= None, skip: int = 0, limit: int = 10, search:Annotated[str, None]=None):
    start = time.time()
    response = parkinglotutil.parkinglotlist(lat=lat, lng=lng, skip=skip,limit=limit, search=search)
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

@parkinglotrouter.post("/parkingarea/parkingdata/exit/manual")
def parking_exit(img: UploadFile, parkingdataid: Annotated[int, Form()]):
    start = time.time()
    response = parkinglotutil.manual_exit(img=img, parkingdataid=parkingdataid)
    util.time_message(f"Manual Exit for parkingdata {parkingdataid}",start)
    return response