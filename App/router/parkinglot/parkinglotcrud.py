from ...database import connectdb, models
from ...schema import data
from ...util import time_message
import time
from sqlalchemy import func
from sqlalchemy.sql import or_, and_
from sqlalchemy.sql.functions import now
from math import cos, pi

#GET
def get_parkingdata_by_id(id:int) -> models.ParkingData:
    try:
        with connectdb.session() as db:
            dbparkingdata = db.query(models.ParkingData).filter(models.ParkingData.id==id).first()
            return dbparkingdata
    except Exception as e:
        raise e

def get_parkinglot_by_id(id:int) -> models.ParkingLot:
    try:
        with connectdb.session() as db:
            dbparkinglot = db.query(models.ParkingLot).filter(models.ParkingLot.id==id).first()
            return dbparkinglot
    except Exception as e:
        raise e

def get_parkingarea_by_id(id:int) -> models.ParkingArea:
    try:
        with connectdb.session() as db:
            dbparkingarea = db.query(models.ParkingArea).filter(models.ParkingArea.id==id).first()
            return dbparkingarea
    except Exception as e:
        raise e
    
def get_parkingarea_by_parkinglotid(parkinglotid: int):
    try:
        with connectdb.session() as db:
            dbparkingarea = db.query(models.ParkingArea).filter(models.ParkingArea.parkinglotid==parkinglotid).all()
            return dbparkingarea
    except Exception as e:
        raise e
    
def get_parkinglot_list(search:str, lat:float, lng:float, skip: int=0, limit: int=10):
    try:
        with connectdb.session() as db:
            
            car_remaing_space = db.query(models.ParkingArea.parkinglotid, func.sum(models.ParkingArea.remainingspace).label("car_remaining_space")
                                        ).filter(models.ParkingArea.iscar == 1   
                                        ).group_by(models.ParkingArea.parkinglotid
                                        ).subquery()
                                        
            motorbike_remaing_space = db.query(models.ParkingArea.parkinglotid, func.sum(models.ParkingArea.remainingspace).label("motorbike_remaining_space")
                                        ).filter(models.ParkingArea.iscar == 0   
                                        ).group_by(models.ParkingArea.parkinglotid
                                        ).subquery()
            
            if((lat != None) | (lng != None)):
                #5km offset
                latOffset = 5/111 
                lngOffset = 5/(111 * cos(lat * pi / 180))
                
                south = lat-latOffset
                north = lat+latOffset
                west = lng-lngOffset
                east = lng+lngOffset
                
                if(search != None):
                    if((not search.isspace()) & (search != "")):
                        return db.query(models.ParkingLot, car_remaing_space.c.car_remaining_space, motorbike_remaing_space.c.motorbike_remaining_space
                                        ).outerjoin(car_remaing_space, car_remaing_space.c.parkinglotid == models.ParkingLot.id
                                        ).outerjoin(motorbike_remaing_space, motorbike_remaing_space.c.parkinglotid == models.ParkingLot.id
                                        ).filter(or_(
                                            and_(models.ParkingLot.lat.between(south, north), 
                                                models.ParkingLot.lng.between(west, east)),
                                            models.ParkingLot.name.like("%{}%".format(search)),
                                            models.ParkingLot.address.like("%{}%".format(search)))
                                        ).offset(offset=skip
                                        ).limit(limit=limit
                                        ).all()
                
                return db.query(models.ParkingLot, car_remaing_space.c.car_remaining_space, motorbike_remaing_space.c.motorbike_remaining_space
                                    ).outerjoin(car_remaing_space, car_remaing_space.c.parkinglotid == models.ParkingLot.id
                                    ).outerjoin(motorbike_remaing_space, motorbike_remaing_space.c.parkinglotid == models.ParkingLot.id
                                    ).filter(models.ParkingLot.lat.between(south, north), models.ParkingLot.lng.between(west, east)
                                    ).offset(offset=skip
                                    ).limit(limit=limit
                                    ).all()
                                
            if(search != None):
                if((not search.isspace()) & (search != "") & (search != None)):
                    return db.query(models.ParkingLot, car_remaing_space.c.car_remaining_space, motorbike_remaing_space.c.motorbike_remaining_space
                                    ).outerjoin(car_remaing_space, car_remaing_space.c.parkinglotid == models.ParkingLot.id
                                    ).outerjoin(motorbike_remaing_space, motorbike_remaing_space.c.parkinglotid == models.ParkingLot.id
                                    ).filter(or_(
                                        models.ParkingLot.name.like("%{}%".format(search)),
                                        models.ParkingLot.address.like("%{}%".format(search)))
                                    ).offset(offset=skip
                                    ).limit(limit=limit
                                    ).all()
            return db.query(models.ParkingLot, car_remaing_space.c.car_remaining_space, motorbike_remaing_space.c.motorbike_remaining_space
                                    ).outerjoin(car_remaing_space, car_remaing_space.c.parkinglotid == models.ParkingLot.id
                                    ).outerjoin(motorbike_remaing_space, motorbike_remaing_space.c.parkinglotid == models.ParkingLot.id
                                    ).offset(offset=skip
                                    ).limit(limit=limit
                                    ).all()
    except Exception as e:
        raise e
    
def get_last_parkingdata_by_licensenumber(licensenumber: str, parkingareaid:int):

    with connectdb.session() as db:
        response = db.query(models.ParkingData).filter(models.ParkingData.license == licensenumber, 
                                                       models.ParkingData.parkingareaid == parkingareaid).order_by(models.ParkingData.id.desc()).first()
        
        return response
    
def get_last_parkingdata_by_userid(userid: int, parkingareaid:int):

    with connectdb.session() as db:
        response = db.query(models.ParkingData).filter(models.TransactionDetail.parkingdataid == models.ParkingData.id, models.TransactionDetail.userid == userid,
                                                       models.ParkingData.parkingareaid==parkingareaid).order_by(models.ParkingData.id.desc()).first()
        
        return response


#UPDATE

def areacheckin(parkingareaid:int) -> models.ParkingArea:
    try:
        with connectdb.session() as db:
            dbparkingarea = get_parkingarea_by_id(id=parkingareaid)
            dbparkingarea.remainingspace -= 1
            db.add(dbparkingarea)
            db.commit()
            db.refresh(dbparkingarea)
            return dbparkingarea
    except Exception as e:
        raise e
    
def areacheckout(parkingareaid:int) -> models.ParkingArea:
    try:
        with connectdb.session() as db:
            dbparkingarea = get_parkingarea_by_id(id=parkingareaid)
            dbparkingarea.remainingspace += 1
            db.add(dbparkingarea)
            db.commit()
            db.refresh(dbparkingarea)
            return dbparkingarea
    except Exception as e:
        raise e
    
def update_parkingdata_manualcheck(parkingdataid:int, manualcheckid:int):
    try:
        with connectdb.session() as db:
            dbparkingdata = get_parkingdata_by_id(id=parkingdataid)
            dbparkingdata.manualcheckid = manualcheckid
            db.add(dbparkingdata)
            db.commit()
            db.refresh(dbparkingdata)
            return dbparkingdata
    except Exception as e:
        raise e
        
def update_parkinglot(parkinglotid:int, name:str, address:str, lat:float, lng:float, dayfeemotorbike: float, nightfeemotorbike: float, carfee: float, img_path:str):
    try:
        with connectdb.session() as db:
            dbparkinglot = get_parkinglot_by_id(id=parkinglotid)
            if(dbparkinglot.name != name):
                dbparkinglot.name = name
            if(dbparkinglot.address != address):
                dbparkinglot.address = address
            if(dbparkinglot.lat != lat):
                dbparkinglot.lat = lat
            if(dbparkinglot.lng != lng):
                dbparkinglot.lng = lng
            if(dbparkinglot.dayfeemotorbike != dayfeemotorbike):
                dbparkinglot.dayfeemotorbike = dayfeemotorbike
            if(dbparkinglot.nightfeemotorbike != nightfeemotorbike):
                dbparkinglot.nightfeemotorbike = nightfeemotorbike
            if(dbparkinglot.carfee != carfee):
                dbparkinglot.carfee = carfee
            if(img_path):
                dbparkinglot.imagepath = img_path
            db.add(dbparkinglot)
            db.commit()
            db.refresh(dbparkinglot)
            return dbparkinglot
    except Exception as e:
        raise e
    
def update_parkingarea(img_path:str, parkingareaid:int, area:str, maxspace:int, remainingspace:int, iscar:bool):
    try:
        with connectdb.session() as db:
            dbparkingarea = get_parkingarea_by_id(id=parkingareaid)
            if(dbparkingarea.area != area):
                dbparkingarea.area = area
            if(dbparkingarea.maxspace != maxspace):
                dbparkingarea.maxspace = maxspace
            if(dbparkingarea.remainingspace != remainingspace):
                dbparkingarea.remainingspace = remainingspace
            if(dbparkingarea.iscar != iscar):
                dbparkingarea.iscar = iscar
            if(img_path):
                dbparkingarea.imagepath = img_path
            db.add(dbparkingarea)
            db.commit()
            db.refresh(dbparkingarea)
            return dbparkingarea
    except Exception as e:
        raise e
    

def parking_exit(exit_image: models.Image, dbparkingdata:models.ParkingData):

    with connectdb.session() as db:
        dbparkingdata.eximage=exit_image
        dbparkingdata.exit_time = now()
        db.add(dbparkingdata)
        db.commit()
        db.refresh(dbparkingdata)
        
        return dbparkingdata

#CREATE
def create_parkinglot(name:str, address:str, lat:float, lng:float, dayfeemotorbike: float, nightfeemotorbike: float, carfee: float, img_path:str):
    try:
        with connectdb.session() as db:
            newparkinglot = models.ParkingLot(name=name, address=address, lat=lat, lng=lng, dayfeemotorbike=dayfeemotorbike, 
                                              nightfeemotorbike=nightfeemotorbike, carfee=carfee, imagepath=img_path)
            db.add(newparkinglot)
            db.commit()
            db.refresh(newparkinglot)
            return newparkinglot
    
    except Exception as e:
        raise e
    
def create_parkingarea(area:str, maxspace:int, remainingspace:int, parkinglotid:int, iscar:bool, img_path:str):
    try:
        with connectdb.session() as db:
            newparkingarea = models.ParkingArea(area=area, maxspace= maxspace, remainingspace= remainingspace, parkinglotid=parkinglotid, iscar=iscar, imagepath=img_path)
            db.add(newparkingarea)
            db.commit()
            db.refresh(newparkingarea)
            return newparkingarea
    
    except Exception as e:
        raise e
    
def parking_entry(license_number:str, entry_image_id: int, parkingareaid:int):

    with connectdb.session() as db:
        dbparkingdata = models.ParkingData(license=license_number, entry_img=entry_image_id, entry_time=now(), parkingareaid=parkingareaid)
        db.add(dbparkingdata)
        db.commit()
        db.refresh(dbparkingdata)

        return dbparkingdata
    
def create_manual_check(cid_img_path:str, cavet_img_path:str) -> models.ManualCheck:
    try:
        with connectdb.session() as db:
            dbmanualcheck = models.ManualCheck(cid_image_path=cid_img_path, cavet_image_path = cavet_img_path)
            db.add(dbmanualcheck)
            db.commit()
            db.refresh(dbmanualcheck)
            return dbmanualcheck
    except Exception as e:
        raise e