from fastapi import UploadFile
from ... import util
import os
from ...licensedetection.LP_recognition import LP_recognition
from ...database import crud
from pathlib import Path
from datetime import datetime, time
from ..user import usercrud
from ...auth import authcrud
from . import parkinglotcrud
from dateutil.relativedelta import relativedelta

def parking_entry(img: UploadFile, parkingareaid:int, userid:int):
    imgtime = datetime.now()
    datetimename = str(imgtime).replace(" ","_").replace(":","_").replace("-","_").replace(".","_")
    img.filename = "img{}.png".format(datetimename)
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkinglotcrud.areacheckin(parkingareaid=parkingareaid)
    parkingdb = crud.parking_entry(license_number=licensedb.license_number, entry_image_id=dbimage.id, parkingareaid=parkingareaid)
    dbuser = authcrud.get_user_by_userid(id=userid)
    usercrud.create_transaction(user=dbuser, balancechange=0, description="{} pay for their parking fee with license {} at the parkinglot has address {}".format(dbuser.id, licensedb.license_number, parkinglotcrud.get_parkingarea_by_id(parkingareaid).area), parkingdataid=parkingdb.id)
    return parkingdb

def parking_exit(img: UploadFile, parkingareaid:int, userid:int):
    imgtime = datetime.now()
    datetimename = str(imgtime).replace(" ","_").replace(":","_").replace("-","_").replace(".","_")
    img.filename = "img{}.png".format(datetimename)
    parkingareadb = parkinglotcrud.get_parkingarea_by_id(parkingareaid)
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_exit(license_number=licensedb.license_number, exit_image=dbimage, parkingareaid=parkingareaid)
    parkinglotdb = parkinglotcrud.get_parkinglot_by_id(parkingareadb.parkinglotid)
    
    entrytime = parkingdb.entry_time
    exittime = parkingdb.exit_time
    parkingtime = exittime - entrytime
    parkinghour = parkingtime.seconds//3600
    if(parkingareadb.iscar):
        fee = feecalculator(feetype=parkinglotdb.carfee, parkinghour=parkinghour)
    else:
        dayentry = isday(entrytime)
        dayexit = isday(exittime)
        if parkinghour < 12:
            if(dayentry):
                night = datetime.combine(entrytime.date(),time(hour=18))
                isdaylonger = ((night-entrytime)>(exittime-night))
                if(dayexit or isdaylonger):
                    fee = feecalculator(parkinglotdb.dayfeemotorbike, parkinghour=parkinghour)
                else:
                    fee = feecalculator(parkinglotdb.nightfeemotorbike, parkinghour=parkinghour)
            else:
                night = datetime.combine(exittime.date(),time(hour=6))
                isdaylonger = ((night-entrytime)<(exittime-night))
                if(dayexit and isdaylonger):
                    fee = feecalculator(parkinglotdb.dayfeemotorbike, parkinghour=parkinghour)
                else:
                    fee = feecalculator(parkinglotdb.nightfeemotorbike, parkinghour=parkinghour)
        else:
            fee = 0.0
            day = parkinghour//24
            fee += (3*parkinglotdb.dayfeemotorbike+3*parkinglotdb.nightfeemotorbike)*day
            if(dayentry):
                fee += feecalculator(parkinglotdb.dayfeemotorbike, (datetime.combine(entrytime.date(),time(hour=18))-entrytime))
            else:
                fee += feecalculator(parkinglotdb.nightfeemotorbike, ((datetime.combine(entrytime.date(),time(hour=6))+relativedelta(days=1))-entrytime))
                
            if(dayexit):
                fee += feecalculator(parkinglotdb.dayfeemotorbike, (exittime-datetime.combine(exittime.date(),time(hour=6))))
            else:
                fee += feecalculator(parkinglotdb.nightfeemotorbike, (exittime-datetime.combine(exittime.date(),time(hour=18))))
            
    fee = round(fee,2)
    #fee payment
    usercrud.update_transaction_change(parkingdataid=parkingdb.id, userid=userid, change=-fee)
    usercrud.update_userbalance_by_userid(user=authcrud.get_user_by_userid(id=userid), balancechange=-fee)
    parkinglotcrud.areacheckout(parkingareaid=parkingareaid)
    return parkingdb

def isday(vartime: datetime) -> bool:
    return (vartime>datetime.combine(vartime.date(),time(hour=6)) and vartime<datetime.combine(vartime.date(),time(hour=18)))

def feecalculator(feetype:float, parkinghour:int):
    return feetype*((parkinghour//4)+1)


