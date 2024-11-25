from sqlalchemy import Column

from connectdb import Base
class Cavet(Base):
    __tablename__ = "cavets"
    
    
    owner_fullname = Column