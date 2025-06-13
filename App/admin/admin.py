from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import JSONResponse
from typing import Annotated
from . import adminutil
from ..schema import data
from ..auth import authcontroller, authcrud
from ..router.parkinglot.parkinglot import parkinglotrouter
from fastapi.staticfiles import StaticFiles
from ..util import time_message
import time

adminapi = FastAPI(servers=[{"url": "/admin"},{"url":""}], dependencies=[Depends(authcontroller.check_adminpage_access)])
adminapi.include_router(parkinglotrouter)
#TODO: Admin page, function

adminapi.mount("/adminstatic",StaticFiles(directory="adminstatic"), name="adminstatic")

@adminapi.get("/", tags=["user"])
def get_current_admin(user: Annotated[data.User, Depends(authcontroller.check_adminpage_access)]):
    return user

@adminapi.get("/role/details", tags=["role"])
def get_role_detail(roleid: int):
    start = time.time()
    response = authcrud.get_role_by_id(id=roleid)
    time_message(f"get role with id {roleid} detail",start)
    return response

@adminapi.post("/user/setrole", tags=["user"])
def set_role(username:Annotated[str, Form()], rolename: Annotated[str, Form()]):
    """
    Set user's role level

    Parameters:\n
        username (str): Username to set role
        role_level (int): Desired user level for this user

    Returns:\n
        JSONResponse: A JSON response containing a success message if set role is successful,
        or an error message if set role fails.
    """
    try:
        start = time.time()
        result = adminutil.update_user_role(username=username, rolename=rolename)
        time_message(f"user {username} role set to {rolename}",start)
        return JSONResponse(content=result, status_code=200)
    
    except Exception as e:
        raise e
      
"""@adminapi.get("/docs",tags=["get docs"], include_in_schema=False)
async def getdoc():
    try:
        return get_swagger_ui_html(openapi_url="/admin/admin.json", title="Admin apis docs")
    except Exception:
        return RedirectResponse("/docs")
        
@adminapi.get("/admin.json",tags=["get docs"], include_in_schema=False)
async def openapijson():
    return adminapi.openapi()"""