from fastapi import UploadFile, HTTPException
from ... import util
import os
from ...licensedetection.LP_recognition import LP_recognition
from ...database import crud, models
from pathlib import Path
from datetime import datetime, time
from ..user import usercrud
from ...auth import authcrud
from . import parkinglotcrud
from dateutil.relativedelta import relativedelta
from ...schema import data
from sqlalchemy import null

def parking_entry(img: UploadFile, parkingareaid:int, userid:int, detected:str):
    try:
        relpath = util.image_autonaming(img=img, destination_directory="parkingdataimage", admin_perm=True)
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        dbimage = crud.create_image(relpath, type="detect")
        licensedb = crud.create_detectedlicense(license_number=detected, image_id=dbimage.id)
        checkparkingdb = parkinglotcrud.get_last_parkingdata_by_licensenumber(licensenumber=licensedb.license_number, parkingareaid=parkingareaid)
        if(checkparkingdb):
            if(checkparkingdb.exit_time == None):
                raise HTTPException(status_code=400, detail="data existed")
        parkingdb = parkinglotcrud.parking_entry(license_number=licensedb.license_number, entry_image_id=dbimage.id, parkingareaid=parkingareaid)
        parkinglotcrud.areacheckin(parkingareaid=parkingareaid)
        dbuser = authcrud.get_user_by_userid(id=userid)
        usercrud.create_transaction(user=dbuser, balancechange=0, description="{} pay for their parking fee with license {} at the parkinglot has address {}".format(dbuser.username, licensedb.license_number, parkinglotcrud.get_parkingarea_by_id(parkingareaid).area), parkingdataid=parkingdb.id)
        return parkingdb
    except Exception as e:
        raise e

def parking_exit(img: UploadFile, parkingareaid:int, userid:int, detected:str):
    try:
        parkingareadb = parkinglotcrud.get_parkingarea_by_id(parkingareaid)
        relpath = util.image_autonaming(img=img, destination_directory="parkingdataimage", admin_perm=True)
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        dbimage = crud.create_image(relpath, type="detect")
        licensedb = crud.create_detectedlicense(license_number=detected, image_id=dbimage.id)
        entryparkingdb = parkinglotcrud.get_last_parkingdata_by_licensenumber(licensenumber=licensedb.license_number, parkingareaid=parkingareaid)
        if(not entryparkingdb):
            raise HTTPException(status_code=400, detail="parkingdata with userid {} not found".format(userid))
        
        if(entryparkingdb.exit_time):
            raise HTTPException(status_code=400, detail="parkingdata with userid {} not found".format(userid))
        
        parkingdb = entryparkingdb
        if (not entryparkingdb.manualcheckid):
            transactiondb = usercrud.get_transaction_by_userid_parkingid(userid=userid, parkingdataid=entryparkingdb.id)
            if(not transactiondb):
                raise HTTPException(status_code=400, detail="parkingdata with userid {} not found".format(userid))
        
        parkingdb = parkinglotcrud.parking_exit(exit_image=dbimage, dbparkingdata=entryparkingdb)
        fee = calculate_fee(parkingdb=parkingdb, parkingareadb=parkingareadb)
        #fee payment
        usercrud.update_transaction_change(parkingdataid=parkingdb.id, change=-fee)
        usercrud.update_userbalance(user=authcrud.get_user_by_userid(id=userid), balancechange=-fee)
        parkinglotcrud.areacheckout(parkingareaid=parkingareaid)
        return parkingdb
    except Exception as e:
        raise e

def isday(vartime: datetime) -> bool:
    return (vartime>datetime.combine(vartime.date(),time(hour=6)) and vartime<datetime.combine(vartime.date(),time(hour=18)))

def feecalculator(feetype:float, parkinghour:int):
    return feetype*((parkinghour//4)+1)

def parkinglotlist(search:str, lat:float, lng:float, skip: int = 0, limit: int = 10):
    response = list[data.ParkingLot]()
    dbresponse = parkinglotcrud.get_parkinglot_list(search=search, lat=lat, lng=lng, skip=skip, limit=limit)
    
    for parkinglot in dbresponse:
        parkinglottuple = parkinglot.tuple()
        parkinglotdata = parkinglottuple[0]
                    
        dataParkingLot = data.ParkingLot(id=parkinglotdata.id,name=parkinglotdata.name, address=parkinglotdata.address, lat=parkinglotdata.lat, lng = parkinglotdata.lng,  dayfeemotorbike=parkinglotdata.dayfeemotorbike, nightfeemotorbike=parkinglotdata.nightfeemotorbike, carfee=parkinglotdata.carfee, car_remaining_space=0, motorbike_remaining_space=0, image_path="")
        
        if(parkinglottuple[1]):
            dataParkingLot.car_remaining_space = parkinglottuple[1]
        
        if(parkinglottuple[2]):
            dataParkingLot.motorbike_remaining_space = parkinglottuple[2]
            
        if(parkinglotdata.imagepath):
            dataParkingLot.image_path = parkinglotdata.imagepath
        
        response.append(dataParkingLot)
        
    return response

def create_parkinglot(name:str, address:str, lat:float, lng:float, dayfeemotorbike: float=0, nightfeemotorbike: float=0, carfee: float=0, img: UploadFile = None):
    relpath=""
    if(img):
        relpath = util.image_autonaming(img=img, destination_directory="parkinglotimage")
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
    parkinglotdb = parkinglotcrud.create_parkinglot(name=name, address=address, lat=lat, lng=lng,
                                                            dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee, img_path=relpath)
    return parkinglotdb

def create_parkingarea(parkinglotid:int, area:str, maxspace:int, remainingspace:int, iscar:bool, img: UploadFile = None):
    if(remainingspace>maxspace):
        raise HTTPException(status_code=400, detail="remaining space cannot higher than max space")
    relpath=""
    if(img):
        relpath = util.image_autonaming(img=img, destination_directory="parkinglotimage")
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
    parkingareadb = parkinglotcrud.create_parkingarea(parkinglotid=parkinglotid, area=area, maxspace=maxspace, remainingspace=remainingspace, iscar=iscar, img_path=relpath)
    return parkingareadb

def update_parkinglot(parkinglotid: int, name:str, address:str, lat:float, lng:float, dayfeemotorbike: float, nightfeemotorbike: float, carfee: float, img: UploadFile = None):
    relpath=""
    if(img):
        relpath = util.image_autonaming(img=img, destination_directory="parkinglotimage")
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
    parkinglotdb = parkinglotcrud.update_parkinglot(parkinglotid=parkinglotid, name=name, address=address, lat=lat, lng=lng,
                                                            dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee, img_path=relpath)
    return parkinglotdb
        
def update_parkingarea(parkingareaid: int, area:str, maxspace:int, remainingspace:int, iscar:bool, img: UploadFile = None):
    if(remainingspace>maxspace):
        raise HTTPException(status_code=400, detail="remaining space cannot higher than max space")
    relpath=""
    if(img):
        relpath = util.image_autonaming(img=img, destination_directory="parkinglotimage")
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
    parkingareadb = parkinglotcrud.update_parkingarea(parkingareaid=parkingareaid, area=area, maxspace=maxspace, remainingspace=remainingspace, iscar=iscar, img_path=relpath)
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
    
def calculate_fee(parkingdb: models.ParkingData, parkingareadb: models.ParkingArea):
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
                fee += feecalculator(parkinglotdb.dayfeemotorbike, (datetime.combine(entrytime.date(),time(hour=18))-entrytime).seconds//3600)
            else:
                fee += feecalculator(parkinglotdb.nightfeemotorbike, ((datetime.combine(entrytime.date(),time(hour=6))+relativedelta(days=1))-entrytime).seconds//3600)
                
            if(dayexit):
                fee += feecalculator(parkinglotdb.dayfeemotorbike, (exittime-datetime.combine(exittime.date(),time(hour=6))).seconds//3600)
            else:
                fee += feecalculator(parkinglotdb.nightfeemotorbike, (exittime-datetime.combine(exittime.date(),time(hour=18))).seconds//3600)
            
    return round(fee,2)

def manual_exit(img: UploadFile, parkingdataid: int):
    try:
        parkingdatadb = parkinglotcrud.get_parkingdata_by_id(id=parkingdataid)
        parkingareadb = parkinglotcrud.get_parkingarea_by_id(parkingdatadb.parkingareaid)
        relpath = util.image_autonaming(img=img, destination_directory="parkingdataimage", admin_perm=True)
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        dbimage = crud.create_image(relpath, type="manual")
        
        parkingdb = parkinglotcrud.parking_exit(exit_image=dbimage, dbparkingdata=parkingdatadb)
        fee = calculate_fee(parkingdb=parkingdb, parkingareadb=parkingareadb)
        #fee payment
        transactiondb = usercrud.update_transaction_change(parkingdataid=parkingdb.id, change=-fee)
        usercrud.update_userbalance(user=authcrud.get_user_by_userid(id=transactiondb.userid), balancechange=-fee)
        parkinglotcrud.areacheckout(parkingareaid=parkingareadb.id)
        return parkingdb
    except Exception as e:
        raise e