from fastapi import HTTPException
from . import usercrud
from ...auth import authcrud
from ...database import models
from ...schema import data


def increasechange(username:str, change:float) -> models.UserDetail:
    if change<0.0:
        raise HTTPException(status_code=400, detail="Insert Money Value must be positive")
    userdb = authcrud.get_user_by_username(username=username)
    updateduserdetail = usercrud.update_userbalance(user=userdb, balancechange=change)
    return updateduserdetail

def decreasechange(username:str, change:float) -> models.UserDetail:
    if change<0.0:
        raise HTTPException(status_code=400, detail="Insert Money Value must be positive")
    userdb = authcrud.get_user_by_username(username=username)
    updateduserdetail = usercrud.update_userbalance(user=userdb, balancechange=-change)
    return updateduserdetail

def newuserfeedback(username:str, subject:str, detail:str) -> models.FeedBack:
    dbuser = authcrud.get_user_by_username(username=username)
    return usercrud.create_feedback(user=dbuser, subject=subject, detail=detail)

def update_user_phonenumber(username:str, phonenumber:str):
    if len(phonenumber) != 10:
        raise HTTPException(status_code=400, detail="Phonenumber must have 10 number characters")
    userdb = authcrud.get_user_by_username(username=username)
    updateduserdetail = usercrud.update_userphonenumber(user=userdb, phonenumber=phonenumber)
    return updateduserdetail

def get_user_detail(user: data.User):
    phonenumber = ""
    dbUserDetail = usercrud.get_userdetails_by_userid(userid=user.id)
    if(dbUserDetail.phonenumber):
        phonenumber=dbUserDetail.phonenumber
    dbRole = authcrud.get_role_by_id(id=dbUserDetail.roleid)
    return data.UserDetail(id=dbUserDetail.id, phonenumber=phonenumber, balance=dbUserDetail.balance, role=dbRole.name)