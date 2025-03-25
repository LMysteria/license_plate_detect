from . import authcrud, authconfig
from dotenv import load_dotenv, find_dotenv
from os import getenv, getcwd, path
import subprocess
from fastapi import HTTPException, status, Depends
import re
from datetime import datetime, timedelta, timezone
import jwt
from ..schema import data
from typing import Annotated
from jwt.exceptions import InvalidTokenError

def get_SECRET_KEY() -> str:
    """
    Get JWT SECRET_KEY from env variable, create one if not exist for development

    Returns:
        str: SECRET_KEY use for encode and decode jwt
    """
    keypath = path.join(getcwd(), "App", "keys", "auth.env")
    load_dotenv(find_dotenv(keypath,usecwd=True))
    SECRET_KEY = getenv("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = subprocess.run(["openssl","rand","-hex","32"], stdout=subprocess.PIPE, shell=True).stdout.decode("utf-8").strip()
        with open(keypath,"a") as config:
            config.writelines(f"SECRET_KEY=\"{SECRET_KEY}\"")
    return SECRET_KEY


#get hashed version of password
def get_password_hash(password) -> str:
    """  
    Generate a hashed version of a password.  

    Parameters:  
    password (str): The plain text password to hash.  

    Returns:  
    str: The hashed password.  
    """  
    return authconfig.pwd_context.hash(password)
    

def signup_user(username:str, password:str):
    """
    Create new user

    Parameter:
        - username (str): The desired username for the new user.
        - password (str): The raw password for the new user.

    Raises:
        HTTPException 409: Username already registered
        HTTPException 400: Username empty or contain special character or password not met condition

    Returns:
        models.User: User data (id, username, hashedpassword)
    """
    pattern = r"[a-zA-z0-9]{6,}"
    check_username = re.match(pattern=pattern,string=username)
    if(username==None or username==""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username must not be empty")
    if(not check_username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username must contain atleast 6 character and only non-special character")
    if(check_username[0] != username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username must contain atleast 6 character and only non-special character")
    print(14)
    db_user = authcrud.get_user_by_username(username)
    if(password==None or password==""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password must not be empty")
    check_pw = re.match(pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",string=password)
    if(check_pw == None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password must contain atleast 8 character. At least 1 uppercase character. At least 1 lowercase character. At least 1 digit. At least 1 special character\n")
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already registered")
    newuser = authcrud.create_user(username=username, password=get_password_hash(password))
    return data.User(id=newuser.id, username=username)

#get expires datetime
def get_expires_datetime() -> datetime:
    """  
    Calculate the expiration datetime for the access token.  

    Returns:  
    datetime: The expiration datetime in UTC.  
    """ 
    return (datetime.now(timezone.utc)+timedelta(minutes=authconfig.ACCESS_TOKEN_EXPIRE_MINUTES))

#verify password
def verify_password(plain_password, hashed_password) -> bool:
    """  
    Verify that a plain password matches the hashed password.  

    Parameters:  
    plain_password (str): The plain text password to verify.  
    hashed_password (str): The hashed password to verify against.  

    Returns:  
    bool: True if the password matches the hash, otherwise False.  
    """  
    return authconfig.pwd_context.verify(plain_password, hashed_password)

#create jwt access token
def create_access_token(data: dict) -> str:
    """  
    Create a JWT access token with an expiration time.  

    Parameters:  
    data (Dict[str, any]): The data to encode in the JWT token.  

    Returns:  
    str: The encoded JWT token as a string.  
    """ 
    to_encode = data.copy()
    expire = get_expires_datetime()
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, get_SECRET_KEY(), algorithm=authconfig.ALGORITHM)
    return {"jwt":encoded_jwt, "exp":expire}

#authenticate user
async def authenticate_user(username: str, password: str) -> data.Token:
    """
    Authenticate user via login to gain access

    Parameter:
        - username (str): The username of the user attempting to log in.
        - password (str): The raw password of the user attempting to log in.
        
    Raises:
        HTTPException: status_code 401 if username or password is not correct

    Returns:
        str: access_token
    """
    unauthorized_msg = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="username or password is incorrect",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        db_user = authcrud.get_user_by_username(username)
        print(db_user)
        if not db_user:
            raise unauthorized_msg
        if not verify_password(password, db_user.password):
            raise unauthorized_msg
        userdata = {"sub":db_user.username}
        access_token = create_access_token(data=userdata)
        return data.Token(access_token=access_token["jwt"], token_type="bearer", expire=access_token["exp"])
    except Exception as error:
        raise error

async def get_current_user(token: Annotated[str, Depends(authconfig.oauth2_scheme)]) -> data.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_SECRET_KEY(), algorithms=[authconfig.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        dbuser = authcrud.get_user_by_username(username=username)
        if dbuser is None:
            raise credentials_exception
        return data.User(id=dbuser.id, username=dbuser.username)
    except InvalidTokenError:
        raise credentials_exception

async def check_adminpage_access(user: Annotated[data.User, Depends(get_current_user)]) -> data.User:
    access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access Denied",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        dbadminpage = authcrud.get_access_by_name("adminpage")
        dbuserdetail = authcrud.get_userdetails_by_userid(userid=user.id)
        dbroleAccess = authcrud.get_role_access_by_roleid(id=dbuserdetail.roleid)
        for access in dbroleAccess:
            if access.id == dbadminpage.id:
                return user
        raise access_exception
    except Exception as e:
        raise e