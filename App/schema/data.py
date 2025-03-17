from pydantic import BaseModel
from typing import Annotated

class DetectedLicense(BaseModel):
    license_number: str
    image_id: int
    
class Image(BaseModel):
    path: str
    dataset_id: Annotated[int, None] = None
    
class User(BaseModel):
    id: int
    username: str
    
class Token(BaseModel):
    access_token: str
    token_type: str