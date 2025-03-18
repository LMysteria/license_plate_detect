from fastapi import HTTPException
from . import usercrud
from ...auth import authcrud
from ...database import models

def increasechange(username:str, change:float) -> models.UserDetail:
    if change<0.0:
        raise HTTPException(status_code=400, detail="Insert Money Value must be positive")
    userdb = authcrud.get_user_by_username(username=username)
    updateduserdetail = usercrud.update_userbalance_by_userid(user=userdb, balancechange=change)
    return updateduserdetail

def decreasechange(username:str, change:float) -> models.UserDetail:
    if change<0.0:
        raise HTTPException(status_code=400, detail="Insert Money Value must be positive")
    userdb = authcrud.get_user_by_username(username=username)
    updateduserdetail = usercrud.update_userbalance_by_userid(user=userdb, balancechange=-change)
    return updateduserdetail