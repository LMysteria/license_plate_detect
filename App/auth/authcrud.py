from ..database import connectdb, models
from typing import Annotated
from datetime import datetime
import time
from util import time_message

#GET
def get_user_by_username(username:str) -> models.User:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.User).filter(models.User.username==username).first()
    time_message("Get user with username "+username+" execution time", time.time()-start)
    return response
#

#CREATE
def create_user(username:str, password:str) -> models.User:
    start = time.time()
    
    try:
        with connectdb.session() as db:
            user = models.User(username=username, password=password)
            db.add(user)
            db.commit()
            db.refresh(user)
            
            time_message("Create user execution time", time.time()-start)
            return user
    except:
        return None
