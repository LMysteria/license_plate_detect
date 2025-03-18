from fastapi import UploadFile
from ... import util
import os
from ...licensedetection import LP_recognition
from ...database import crud
from pathlib import Path
from datetime import datetime
from ..user import usercrud
from ...auth import authcrud
from . import parkinglotcrud

def parking_entry(img: UploadFile, parkinglotid:int, userid:int):
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_entry(license_number=licensedb.license_number, entry_image_id=dbimage.id, entry_datetime=datetime.now(), parkinglotid=parkinglotid)
    dbuser = authcrud.get_user_by_userid(id=userid)
    usercrud.create_transaction(user=dbuser, balancechange=0, description="{} pay for their parking fee with license {} at the parkinglot has address {}".format(dbuser.id, licensedb.license_number, parkinglotcrud.get_parkinglot_by_id(parkinglotid).address), parkingid=parkingdb.id)
    return parkingdb

def parking_exit(img: UploadFile, parkinglotid:int, userid:int):
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_exit(license_number=licensedb.license_number, exit_image=dbimage, exit_datetime=datetime.now(), parkinglotid=parkinglotid)
    #missing change calculator
    #usercrud.update_transaction_change(parkingid=parkingdb.id, userid=userid, change=)
    return parkingdb