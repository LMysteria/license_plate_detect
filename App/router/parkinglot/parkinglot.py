from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Annotated
from . import parkinglotcrud, parkinglotutil
from ... import util
import time

parkinglotrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])
ParkinglotUserrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])

@parkinglotrouter.get("/parkingarea/parkingdata")
def get_parkingdata_detail(parkingdataid:int):
    start = time.time()
    response = parkinglotcrud.get_parkingdata_by_id(id=parkingdataid)
    util.time_message("get parking data with id {}".format(parkingdataid), starttime=start)
    return response

@parkinglotrouter.post("/create")
def create_parkinglot(name:Annotated[str, Form()], address:Annotated[str, Form()], 
                      dayfeemotorbike:Annotated[float, Form()], nightfeemotorbike:Annotated[float, Form()], carfee:Annotated[float, Form()],
                      img: Annotated[UploadFile, None] = None):
    return parkinglotutil.create_parkinglot(name=name, address=address, dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee, img=img)

@parkinglotrouter.post("/parkingarea/create")
def create_parkinglot(area:Annotated[str, Form()], maxspace:Annotated[int, Form()], remainingspace:Annotated[int, Form()], 
                      parkinglotid: Annotated[int, Form()], iscar: Annotated[bool, Form()],
                      img: Annotated[UploadFile, None] = None):
    return parkinglotutil.create_parkingarea(area=area, maxspace=maxspace, remainingspace=remainingspace, parkinglotid=parkinglotid, iscar=iscar, img=img)

@parkinglotrouter.post("/parkingarea/parkingdata/entry")
def parking_entry(img: UploadFile, parkingareaid: Annotated[int, Form()], userid: Annotated[int, Form()]):
    return parkinglotutil.parking_entry(img=img, parkingareaid=parkingareaid, userid=userid)

@parkinglotrouter.post("/parkingarea/parkingdata/exit")
def parking_exit(img: UploadFile, parkingareaid: Annotated[int, Form()], userid: Annotated[int, Form()]):
    return parkinglotutil.parking_exit(img=img, parkingareaid=parkingareaid, userid=userid)

@parkinglotrouter.post("/update")
def update_parkingarea_image(parkinglotid: Annotated[int, Form()], name:Annotated[str, Form()], address:Annotated[str, Form()], 
                             dayfeemotorbike:Annotated[float, Form()], nightfeemotorbike:Annotated[float, Form()], carfee:Annotated[float, Form()], 
                             img: Annotated[UploadFile, None] = None):
    return parkinglotutil.update_parkinglot(img=img, parkinglotid=parkinglotid, name=name, address=address,
                                            dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee)

@parkinglotrouter.post("/parkingarea/update")
def update_parkingarea_image(parkingareaid: Annotated[int, Form()], area:Annotated[str, Form()], maxspace:Annotated[int, Form()], remainingspace:Annotated[int, Form()], 
                      iscar: Annotated[bool, Form()], img: Annotated[UploadFile, None] = None):
    return parkinglotutil.update_parkingarea(img=img, parkingareaid=parkingareaid, area=area, maxspace=maxspace, remainingspace=remainingspace, iscar=iscar)

@parkinglotrouter.post("/parkingarea/parkingdata/manualcheck/create")
def parkingdata_manualcheck(cid_img: UploadFile, cavet_img: UploadFile, parkingdataid: Annotated[int, Form()]):
    return parkinglotutil.manual_check(cid_img=cid_img, cavet_img=cavet_img, parkingdataid=parkingdataid)

@ParkinglotUserrouter.get("")
def get_parkinglot_detail(parkinglotid:int):
    return parkinglotcrud.get_parkinglot_by_id(id=parkinglotid)

@ParkinglotUserrouter.get("/list")
def get_parkinglot_list(search: str = "", skip: int = 0, limit: int = 10):
    response = parkinglotutil.parkinglotlist(search=search, skip=skip,limit=limit)
    return response

@ParkinglotUserrouter.get("/parkingarea")
def get_parkingarea_detail(parkingareaid:int):
    return parkinglotcrud.get_parkingarea_by_id(id=parkingareaid)

@ParkinglotUserrouter.get("/parkingarea/list")
def get_parkinglot_list(parkinglotid: int):
    response = parkinglotcrud.get_parkingarea_by_parkinglotid(parkinglotid=parkinglotid)
    return response