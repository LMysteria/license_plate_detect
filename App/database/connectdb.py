from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import find_dotenv, load_dotenv
from os import getenv

#database connection config
load_dotenv(find_dotenv("/App/keys/db.env", usecwd=True))
config={
    "username" : getenv("DBUSERNAME"),
    "password" : getenv("DBPASSWORD"),
    "host" : getenv("DBHOST"),
    "database" : getenv("DATABASE")
}

#check if databae exist
checkengine = create_engine(
    f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}"
)
with checkengine.connect() as con:
    existing_database = con.execute(text("SHOW DATABASES;"))
    existing_database = [d[0] for d in existing_database]
    if config["database"] not in existing_database:
        con.execute(text(f"CREATE DATABASE {config['database']};"))
        print(f"Created database {config['database']}")
    
#connnection engine
engine = create_engine(
    f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}/{config['database']}"
)

#initialize database
Sessionlocal = sessionmaker(autoflush= False, bind= engine, autocommit=False)
Base = declarative_base()

def session():
    """
    Provide database connection session

    Example: 
    With session() as db:
        db.query(*table).first()

    Returns:
        Session: Session to access database
    """
    return Sessionlocal()
