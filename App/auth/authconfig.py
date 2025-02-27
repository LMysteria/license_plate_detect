from passlib.context import CryptContext

#jwt encode config
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAY = 7

#password hash config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
