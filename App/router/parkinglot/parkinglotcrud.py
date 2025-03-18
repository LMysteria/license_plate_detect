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

def create_parkinglot(address:str, maxspace:int, remainingspace:int):
    try:
        with connectdb.session() as db:
            newparkinglot = models.ParkingLot(address=address, maxspace= maxspace, remainingspace= remainingspace)
            db.add(newparkinglot)
            db.commit()
            db.refresh()
            return newparkinglot
    
    except Exception as e:
        raise e
    
