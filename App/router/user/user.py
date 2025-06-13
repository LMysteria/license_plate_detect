from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from typing import Annotated
import time
from ...auth import authcontroller
from ...schema import data
from . import usercrud, userutil
from ...util import time_message

userrouter = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(authcontroller.get_current_user)])

@userrouter.get("/detail")
def get_userdetails(user: Annotated[data.User, userrouter.dependencies[0]]):
    start = time.time()
    response = userutil.get_user_detail(user=user)
    time_message(f"Get user {user.username} detail",start)
    return response

@userrouter.get("/transactions")
def get_userdetails(user: Annotated[data.User, userrouter.dependencies[0]]):
    start = time.time()
    response = usercrud.get_transaction_by_userid(userid=user.id)
    time_message(f"Get transactions for user {user.username}",start)
    return response

@userrouter.get("/transaction")
def get_userdetails(user: Annotated[data.User, userrouter.dependencies[0]], parkingid: int):
    start = time.time()
    response = usercrud.get_transaction_by_userid_parkingid(userid=user.id, parkingdataid=parkingid)
    time_message(f"Get transactions for user {user.username}",start)
    return response

@userrouter.get("/account")
def get_current_user(user: Annotated[data.User, userrouter.dependencies[0]]):
    return user

@userrouter.post("/balance/insert")
def insert_money_to_balance(user: Annotated[data.User, userrouter.dependencies[0]], insertmoney: Annotated[float, Form()]):
    start = time.time()
    response = userutil.increasechange(username=user.username, change=insertmoney)
    time_message(f"Insert money to user {user.username} with amount {insertmoney}",start)
    return response

@userrouter.post("/detail/update")
def update_phonenumber(user: Annotated[data.User, userrouter.dependencies[0]], phonenumber: Annotated[str, Form()]):
    start = time.time()
    response = userutil.update_user_phonenumber(username=user.username, phonenumber=phonenumber)
    time_message(f"update user {user.username} detail",start)
    return response

@userrouter.post("/feedback/create")
def create_feedback(user: Annotated[data.User, userrouter.dependencies[0]], subject:Annotated[str, Form()], detail: Annotated[str, Form()]):
    start = time.time()
    response = userutil.newuserfeedback(username=user.username, subject=subject, detail=detail)
    time_message(f"create feedback from user {user.username}", start)
    return response

