from . import authcrud, authconfig
from dotenv import load_dotenv, find_dotenv
from os import getenv
import subprocess
from fastapi import HTTPException, status
import re

def get_SECRET_KEY() -> str:
    """
    Get JWT SECRET_KEY from env variable, create one if not exist for development

    Returns:
        str: SECRET_KEY use for encode and decode jwt
    """
    load_dotenv(find_dotenv("App/keys/auth.env",usecwd=True))
    SECRET_KEY = getenv("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = subprocess.run(["openssl","rand","-hex","32"], stdout=subprocess.PIPE, shell=True).stdout.decode("utf-8").strip()
        with open("keys/auth.env","a") as config:
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
    

async def signup_user(username:str, password:str) -> str:
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
    pattern = r"[a-zA-z0-9]+"
    check_username = re.match(pattern=pattern,string=username)
    if(username==None or username==""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username must not be empty")
    if(check_username[0] != username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username must contain only non-special character")
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
    return authcrud.create_user(username=username, hashed_password=get_password_hash(password))

