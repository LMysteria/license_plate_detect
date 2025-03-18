from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from typing import Annotated
from ...auth import authcontroller
from ...schema import data
from . import usercrud, userutil

userrouter = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(authcontroller.get_current_user)])

@userrouter.get("/detail")
def get_userdetails(user: Annotated[data.User, userrouter.dependencies[0]]):
    return usercrud.get_userdetails_by_userid(userid=user.id)

@userrouter.get("/account")
def get_current_user(user: Annotated[data.User, userrouter.dependencies[0]]):
    return user

@userrouter.post("/balance/insert")
def insert_money_to_balance(user: Annotated[data.User, userrouter.dependencies[0]], insertmoney: Annotated[float, Form()]):
    response = userutil.increasechange(username=user.username, change=insertmoney)
    return response
    
@userrouter.post("/balance/payment")
def payment(user: Annotated[data.User, userrouter.dependencies[0]], payment: Annotated[float, Form()]):
    response = userutil.increasechange(username=user.username, change=payment)
    return response

@userrouter.post("/feedback/create")
def create_feedback(user: Annotated[data.User, userrouter.dependencies[0]], subject:Annotated[str, Form()], detail: Annotated[str, Form()]):
    response = userutil.newuserfeedback(username=user.username, subject=subject, detail=detail)
    return response