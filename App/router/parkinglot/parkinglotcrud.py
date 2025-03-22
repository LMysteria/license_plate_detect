from ...database import connectdb, models
from ...schema import data
from ...util import time_message
import time

#GET
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

#CREATE
def create_parkinglot(address:str, dayfeemotorbike: float, nightfeemotorbike: float, carfee: float):
    try:
        with connectdb.session() as db:
            newparkinglot = models.ParkingLot(address=address, dayfeemotorbike=dayfeemotorbike, nightfeemotorbike=nightfeemotorbike, carfee=carfee)
            db.add(newparkinglot)
            db.commit()
            db.refresh(newparkinglot)
            return newparkinglot
    
    except Exception as e:
        raise e
    
def create_parkingarea(area:str, maxspace:int, remainingspace:int, parkinglotid:int, iscar:bool):
    try:
        with connectdb.session() as db:
            newparkingarea = models.ParkingArea(area=area, maxspace= maxspace, remainingspace= remainingspace, parkinglotid=parkinglotid, iscar=iscar)
            db.add(newparkingarea)
            db.commit()
            db.refresh(newparkingarea)
            return newparkingarea
    
    except Exception as e:
        raise e
