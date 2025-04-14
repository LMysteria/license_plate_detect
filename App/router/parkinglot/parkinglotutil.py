from fastapi import UploadFile, HTTPException
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
from ...schema import data

def parking_entry(img: UploadFile, parkingareaid:int, userid:int):
    try:
        relpath = util.image_autonaming(img=img, destination_directory="parkingdataimage", admin_perm=True)
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        detected = LP_recognition(img_path=relpath)
        dbimage = crud.create_image(relpath, type="detect")
        licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
        parkinglotcrud.areacheckin(parkingareaid=parkingareaid)
        parkingdb = parkinglotcrud.parking_entry(license_number=licensedb.license_number, entry_image_id=dbimage.id, parkingareaid=parkingareaid)
        dbuser = authcrud.get_user_by_userid(id=userid)
        usercrud.create_transaction(user=dbuser, balancechange=0, description="{} pay for their parking fee with license {} at the parkinglot has address {}".format(dbuser.id, licensedb.license_number, parkinglotcrud.get_parkingarea_by_id(parkingareaid).area), parkingdataid=parkingdb.id)
        return parkingdb
    except Exception as e:
        raise e

def parking_exit(img: UploadFile, parkingareaid:int, userid:int):
    try:
        parkingareadb = parkinglotcrud.get_parkingarea_by_id(parkingareaid)
        relpath = util.image_autonaming(img=img, destination_directory="parkingdataimage", admin_perm=True)
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        detected = LP_recognition(img_path=relpath)
        dbimage = crud.create_image(relpath, type="detect")
        licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
        entryparkingdb = parkinglotcrud.get_last_parkingdata_by_licensenumber(licensenumber=licensedb.license_number, parkingareaid=parkingareaid)
        
        parkingdb = entryparkingdb
        if not entryparkingdb.manualcheckid:
            transactiondb = usercrud.get_transaction_by_userid_parkingid(userid=userid, parkingdataid=entryparkingdb.id)
            if(not transactiondb):
                raise HTTPException(status_code=400, detail="parkingdata with userid {} not found".format(userid))
        
        parkingdb = parkinglotcrud.parking_exit(exit_image=dbimage, dbparkingdata=entryparkingdb)
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
        usercrud.update_userbalance(user=authcrud.get_user_by_userid(id=userid), balancechange=-fee)
        parkinglotcrud.areacheckout(parkingareaid=parkingareaid)
        return parkingdb
    except Exception as e:
        raise e

def isday(vartime: datetime) -> bool:
    return (vartime>datetime.combine(vartime.date(),time(hour=6)) and vartime<datetime.combine(vartime.date(),time(hour=18)))

def feecalculator(feetype:float, parkinghour:int):
    return feetype*((parkinghour//4)+1)

def parkinglotlist(search: str = "", skip: int = 0, limit: int = 10):
    response = list[data.ParkingLot]()
    if not search:
        dbresponse = parkinglotcrud.get_parkinglot_list(skip=skip, limit=limit)
    else:
        dbresponse = parkinglotcrud.get_parkinglot_list(searchpattern="%{}%".format(search),skip=skip, limit=limit)
    
    for parkinglot in dbresponse:
        parkinglottuple = parkinglot.tuple()
        print(parkinglottuple)
        parkinglotdata = parkinglottuple[0]
        response.append(data.ParkingLot(id=parkinglotdata.id,name=parkinglotdata.name, address=parkinglotdata.address, dayfeemotorbike=parkinglotdata.dayfeemotorbike, nightfeemotorbike=parkinglotdata.nightfeemotorbike, carfee=parkinglotdata.carfee, car_remaining_space=parkinglottuple[1], motorbike_remaining_space=parkinglottuple[2], image_path=parkinglotdata.imagepath))
        
    return response

def update_parkinglot_image(img: UploadFile, parkinglotid: int):
        relpath = util.image_autonaming(img=img, destination_directory="parkinglotimage")
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        parkinglotdb = parkinglotcrud.update_parkinglot_image(img_path=relpath, parkinglotid=parkinglotid)
        return parkinglotdb
        
def update_parkingarea_image(img: UploadFile, parkingareaid: int):
        relpath = util.image_autonaming(img=img, destination_directory="parkinglotimage")
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        parkingareadb = parkinglotcrud.update_parkingarea_image(img_path=relpath, parkingareaid=parkingareaid)
        return parkingareadb
    
def manual_check(cid_img: UploadFile, cavet_img: UploadFile, parkingdataid:int):
    try:
        cid_relpath = util.image_autonaming(img=cid_img, destination_directory="cavet_image", admin_perm=True)
        cid_fullpath = os.path.join(os.getcwd(),cid_relpath)
        util.save_upload_file(cid_img, Path(cid_fullpath))
        
        cavet_relpath = util.image_autonaming(img=cavet_img, destination_directory="cid_image", admin_perm=True)
        cavet_fullpath = os.path.join(os.getcwd(),cavet_relpath)
        util.save_upload_file(cavet_img, Path(cavet_fullpath))
        
        dbmanualcheck = parkinglotcrud.create_manual_check(cid_img_path=cid_relpath, cavet_img_path=cavet_relpath)
        if(not dbmanualcheck):
            raise Exception("error in creating dbmanualcheck")
        dbparkingdata = parkinglotcrud.update_parkingdata_manualcheck(parkingdataid=parkingdataid, manualcheckid=dbmanualcheck.id)
        if(not dbparkingdata.manualcheckid):
            raise Exception("error in updating parkingdata manualcheck id")
        
        return dbparkingdata
        
    except Exception as e:
        raise e