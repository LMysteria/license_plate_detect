from fastapi import UploadFile
from ... import util
import os
from ...licensedetection.LP_recognition import LP_recognition
from ...database import crud
from pathlib import Path
from datetime import datetime
from ..user import usercrud
from ...auth import authcrud
from . import parkinglotcrud

def parking_entry(img: UploadFile, parkingareaid:int, userid:int):
    entrytime = datetime.now()
    datetimename = str(entrytime).replace(" ","_").replace(":","_").replace("-","_").replace(".","_")
    img.filename = "img{}.png".format(datetimename)
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_entry(license_number=licensedb.license_number, entry_image_id=dbimage.id, entry_datetime=entrytime, parkingareaid=parkingareaid)
    dbuser = authcrud.get_user_by_userid(id=userid)
    usercrud.create_transaction(user=dbuser, balancechange=0, description="{} pay for their parking fee with license {} at the parkinglot has address {}".format(dbuser.id, licensedb.license_number, parkinglotcrud.get_parkingarea_by_id(parkingareaid).area), parkingdataid=parkingdb.id)
    return parkingdb

def parking_exit(img: UploadFile, parkingareaid:int, userid:int):
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_exit(license_number=licensedb.license_number, exit_image=dbimage, exit_datetime=datetime.now(), parkingareaid=parkingareaid)
    #missing change calculator
    #usercrud.update_transaction_change(parkingdataid=parkingdb.id, userid=userid, change=)
    return parkingdb