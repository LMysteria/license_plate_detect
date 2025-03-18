from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from typing import Annotated
from . import adminutil
from ..schema import data
from ..auth import authcontroller

adminapi = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, servers=[{"url": "/admin"}])
#TODO: Admin page, function

@adminapi.put("/role/setrole", tags=["Users"])
def set_role(username:Annotated[str, Form()], rolename: Annotated[str, Form()], admin: Annotated[data.User, Depends(authcontroller.check_adminpage_access)]):
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
        result = adminutil.update_user_role(username=username, rolename=rolename)

        return JSONResponse(content=result, status_code=200)
    
    except Exception as e:
        raise e
      
@adminapi.get("/docs",tags=["get docs"], include_in_schema=False)
async def getdoc():
    """
    Get Fastapi admin docs with authentication

    Returns:
        html: fastapi docs html
        redirect: access denied, redirect to api docs
    """
    try:
        """token = request._cookies.get("token")
        username = await authcontroller.verify_admin(token=token)"""
        return get_swagger_ui_html(openapi_url="/admin/admin.json", title="Admin apis docs")
    except Exception:
        return RedirectResponse("/docs")
        
@adminapi.get("/admin.json",tags=["get docs"], include_in_schema=False)
async def openapijson():
    """
    create openapi.json docs

    Returns:
        html_json: openapi.json
    """
    """token = request._cookies.get("token")
    username = await authcontroller.verify_admin(token=token)"""
    return adminapi.openapi()