from fastapi import APIRouter, UploadFile, File, Path, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from . import parkinglotcrud, parkinglotutil

parkinglotrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])
ParkinglotUserrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])

@parkinglotrouter.get("/{parkinglotid}/detail")
def get_parkinglot_detail(parkinglotid:Annotated[int, Path()]):
    return parkinglotcrud.get_parkinglot_by_id(id=parkinglotid)

@parkinglotrouter.get("/parkingdata/{parkingdataid}")
def get_parkinglot_detail(parkingdataid:Annotated[int, Path()]):
    return parkinglotcrud.get_parkingdata_by_id(id=parkingdataid)

@parkinglotrouter.post("/create")
def create_parkinglot(name:Annotated[str, Form()], address:Annotated[str, Form()], dayfeemotorbike:Annotated[float, Form()], nightfeemotorbike:Annotated[float, Form()], carfee:Annotated[float, Form()]):
    return parkinglotcrud.create_parkinglot(name=name, address=address, dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee)

@parkinglotrouter.get("/parkingarea/{parkingareaid}")
def get_parkinglot_detail(parkingareaid:Annotated[int, Path()]):
    return parkinglotcrud.get_parkingarea_by_id(id=parkingareaid)

@parkinglotrouter.post("/parkingarea/create")
def create_parkinglot(area:Annotated[str, Form()], maxspace:Annotated[int, Form()], remainingspace:Annotated[int, Form()], parkinglotid: Annotated[int, Form()], iscar: Annotated[bool, Form()]):
    return parkinglotcrud.create_parkingarea(area=area, maxspace=maxspace, remainingspace=remainingspace, parkinglotid=parkinglotid, iscar=iscar)

@parkinglotrouter.post("/parkingarea/{parkingareaid}/parkingdata/create/entry")
def parking_entry(img: UploadFile, parkingareaid: Annotated[int, Path()], userid: int):
    return parkinglotutil.parking_entry(img=img, parkingareaid=parkingareaid, userid=userid)

@parkinglotrouter.post("/parkingarea/{parkingareaid}/parkingdata/create/exit")
def parking_exit(img: UploadFile, parkingareaid: Annotated[int, Path()], userid: int):
    return parkinglotutil.parking_exit(img=img, parkingareaid=parkingareaid, userid=userid)

@parkinglotrouter.post("/{parkinglotid}/update/image")
def update_parkingarea_image(img: UploadFile, parkinglotid: Annotated[int, Path()]):
    return parkinglotutil.update_parkinglot_image(img=img, parkinglotid=parkinglotid)

@parkinglotrouter.post("/parkingarea/{parkingareaid}/update/image")
def update_parkingarea_image(img: UploadFile, parkingareaid: Annotated[int, Path()]):
    return parkinglotutil.update_parkingarea_image(img=img, parkingareaid=parkingareaid)

@parkinglotrouter.post("/parkingdata/{parkingdataid}/create/manualcheck")
def parkingdata_manualcheck(cid_img: UploadFile, cavet_img: UploadFile, parkingdataid: Annotated[int, Path()]):
    return parkinglotutil.manual_check(cid_img=cid_img, cavet_img=cavet_img, parkingdataid=parkingdataid)

@ParkinglotUserrouter.get("/list")
def get_parkinglot_list(search: str = "", skip: int = 0, limit: int = 10):
    response = parkinglotutil.parkinglotlist(search=search, skip=skip,limit=limit)
    return response

@ParkinglotUserrouter.get("/{parkinglotid}/parkingarea/list")
def get_parkinglot_list(parkinglotid: Annotated[int, Path()]):
    response = parkinglotcrud.get_parkingarea_by_parkinglotid(parkinglotid=parkinglotid)
    return response