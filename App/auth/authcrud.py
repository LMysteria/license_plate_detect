from ..database import connectdb, models
from typing import Annotated
from datetime import datetime
import time
from ..util import time_message
from ..router.user.usercrud import get_userdetails_by_userid

#GET
def get_user_by_username(username:str) -> models.User:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.User).filter(models.User.username==username).first()
    time_message("Get user with username {} execution time".format(username), time.time()-start)
    return response

def get_user_by_userid(id:int) -> models.User:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.User).filter(models.User.id==id).first()
    time_message("Get user with id {} execution time".format(id), time.time()-start)
    return response

def get_role_by_name(name:str) -> models.Role:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.Role).filter(models.Role.name == name).first()
        if (not response and name == "user"):
            response = create_role(name="user", description="standard user access")
        if (not response and name == "admin"):
            response = create_role(name="admin", description="standard admin access")
    time_message("Get role {} execution time".format(name), time.time()-start)
    return response

def get_role_by_id(id:int) -> models.Role:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.Role).filter(models.Role.id == id).first()
        time_message("Get role with id {} execution time".format(id), time.time()-start)
    return response

def get_role_access_by_roleid(id:int):
    start = time.time()
    
    with connectdb.session() as db:
        dbrole = db.query(models.Role).filter(models.Role.id == id).first()
        time_message("Get role with id {} execution time".format(id), time.time()-start)
        response = dbrole.roleAccess
    return response
    

def get_access_by_name(name:str) -> models.Access:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.Access).filter(models.Access.name == name).first()
        if (not response and name == "standard"):
            response = create_access(name="standard", description="standard user access")
        if (not response and name == "adminpage"):
            response = create_access(name="adminpage", description="adminpage access")
    time_message("Get access {} execution time".format(name), time.time()-start)
    return response

#UPDATE
def update_role(user: models.User, role:models.Role) -> bool:
    start = time.time()
    try:
        with connectdb.session() as db:
            userdetail = get_userdetails_by_userid(userid=user.id)
            userdetail.roleid = role.id
            db.add(userdetail)
            db.commit()
            db.refresh()
            time_message("Update user {} with role {} execution time".format(user.username, role.name), time.time()-start)
            return True
    except Exception as e:
        return e

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
    except Exception as e:
        raise e

def create_user_details(userid:int) -> models.UserDetail:
    start = time.time()
    try:
        with connectdb.session() as db:
            db_userrole = get_role_by_name(name="user")
            db_userdetails = models.UserDetail(id=userid, roleid=db_userrole.id, balance=0)
            db.add(db_userdetails)
            db.commit()
            db.refresh(db_userdetails)
            
            time_message("Create userdetail with id {} execution time".format(userid), time.time()-start)
            return db_userdetails
    except Exception as e:
        raise e
        
def create_role(name: str, description: str) -> models.Role:
    start = time.time()
    try:

        with connectdb.session() as db:
            dbrole = models.Role(name=name, description=description)
            if dbrole.name == "user":
                standard_access = get_access_by_name(name="standard")
                add_role_access(role=dbrole, access=standard_access)
            if dbrole.name == "admin":
                standard_access = get_access_by_name(name="standard")
                add_role_access(role=dbrole, access=standard_access)
                adminpage_access = get_access_by_name(name="adminpage")
                add_role_access(role=dbrole, access=adminpage_access)
            db.add(dbrole)
            db.commit()
            db.refresh(dbrole)
            time_message("Create role {} execution time".format(name), time.time()-start)
            return dbrole
    except Exception as e:
        raise e
    
def create_access(name: str, description: str) -> models.Access:
    start = time.time()
    try:

        with connectdb.session() as db:
            dbaccess = models.Access(name=name, description=description)
            db.add(dbaccess)
            db.commit()
            db.refresh(dbaccess)
            
            time_message("Create access {} execution time".format(name), time.time()-start)
            return dbaccess
    except Exception as e:
        raise Exception

def add_role_access(role: models.Role, access: models.Access):
    start = time.time()
    try:
        role.roleAccess.append(access)
            
        time_message("Add access {} to role {} execution time".format(access.name, role.name), time.time()-start)
        return True
    except Exception as e:
        raise e