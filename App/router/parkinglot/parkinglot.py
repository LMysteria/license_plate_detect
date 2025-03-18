from fastapi import APIRouter, UploadFile, File, Path, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from ...auth import authcontroller
from ...schema import data
from . import parkinglotcrud, parkinglotutil
import os
import time

parkinglotrouter = APIRouter(prefix="/parkinglot", tags=["parkinglot"])

@parkinglotrouter.get("/{parkinglotid}/detail")
def get_parkinglot_detail(parkinglotid:Annotated[int, Path()]):
    return parkinglotcrud.get_parkinglot_by_id(id=parkinglotid)

@parkinglotrouter.post("/create")
def create_parkinglot(address:str, maxspace:int, remainingspace:int):
    return parkinglotcrud.create_parkinglot(address=address, maxspace=maxspace, remainingspace=remainingspace)

@parkinglotrouter.post("/{parkinglotid}/parkingdata/create/entry")
def parking_entry(img: UploadFile, parkinglotid: Annotated[int, Path()], userid: int):
    return parkinglotutil.parking_entry(img=img, parkinglotid=parkinglotid, userid=userid)

@parkinglotrouter.post("/{parkinglotid}/parkingdata/create/exit")
def parking_exit(img: UploadFile, parkinglotid: Annotated[int, Path()], userid: int):
    return parkinglotutil.parking_exit(img=img, parkinglotid=parkinglotid, userid=userid)