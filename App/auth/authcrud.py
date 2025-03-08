from ..database import connectdb, models
from typing import Annotated
from datetime import datetime
import time
from ..util import time_message

#GET
def get_user_by_username(username:str) -> models.User:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.User).filter(models.User.username==username).first()
    time_message("Get user with username "+username+" execution time", time.time()-start)
    return response

def get_role_by_name(name:str) -> models.User:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.Role).filter(models.Role.name == name).first()
        if (not response and name == "user"):
            response = create_role(name="user", description="standard user access")
    time_message("Get role {} execution time".format(name), time.time()-start)
    return response
        
def get_userdetails_by_userid(userid:int) -> models.UserDetail:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.UserDetail).filter(models.UserDetail.id == userid).first()
    time_message("Get userdetails with id {} execution time".format(userid), time.time()-start)
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
            create_user_details(userid=user.id)
            time_message("Create user {} execution time".format(username), time.time()-start)
            return user
    except:
        print("create_user {} error".format(username))
        return None

def create_user_details(userid:int) -> models.UserDetail:
    start = time.time()
    try:
        with connectdb.session() as db:
            db_userrole = get_role_by_name(name="user")
            db_userdetails = models.UserDetail(id=userid, roleid=db_userrole.id)
            db.add(db_userdetails)
            db.commit()
            db.refresh(db_userdetails)
            
            time_message("Create userdetail with id {} execution time".format(userid), time.time()-start)
            return db_userdetails
    except:
        print("create userdetail with id {} error".format(userid))
        return None
        
def create_role(name: str, description: str) -> models.Role:
    start = time.time()
    try:

        with connectdb.session() as db:
            dbrole = models.Role(name=name, description=description)
            db.add(dbrole)
            db.commit()
            db.refresh(dbrole)
            
            time_message("Create role {} execution time".format(name), time.time()-start)
            return dbrole
    except:
        print("create_role {} error".format(name))
        return None
