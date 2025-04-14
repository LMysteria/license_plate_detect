from pydantic import BaseModel
from typing import Annotated
from datetime import datetime

class DetectedLicense(BaseModel):
    license_number: str
    image_id: int
    
class Image(BaseModel):
    path: str
    dataset_id: Annotated[int, None] = None
    
class User(BaseModel):
    id: int
    username: str
    
class UserDetail(BaseModel):
    id: int
    phonenumber: str
    balance: float
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime
    
class ParkingLot(BaseModel):
    id: int
    name: str
    address: str
    dayfeemotorbike: float
    nightfeemotorbike: float
    carfee: float
    car_remaining_space: int
    motorbike_remaining_space: int
    image_path: str