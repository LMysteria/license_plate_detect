from ...database import connectdb, models
from ...schema import data
from ...util import time_message
import time

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

def create_parkinglot(address:str, maxspace:int, remainingspace:int):
    try:
        with connectdb.session() as db:
            newparkinglot = models.ParkingLot(address=address, maxspace= maxspace, remainingspace= remainingspace)
            db.add(newparkinglot)
            db.commit()
            db.refresh(newparkinglot)
            return newparkinglot
    
    except Exception as e:
        raise e
    
def create_parkingarea(area:str, maxspace:int, remainingspace:int, parkinglotid:int):
    try:
        with connectdb.session() as db:
            newparkingarea = models.ParkingArea(area=area, maxspace= maxspace, remainingspace= remainingspace, parkinglotid=parkinglotid)
            db.add(newparkingarea)
            db.commit()
            db.refresh(newparkingarea)
            return newparkingarea
    
    except Exception as e:
        raise e
