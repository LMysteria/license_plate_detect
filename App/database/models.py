from sqlalchemy import Column, Integer, CHAR, ForeignKey, VARCHAR, Double, DATETIME
from sqlalchemy.orm import relationship
from .connectdb import Base

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    path = Column(CHAR(100), unique=True, index=True, nullable=False)
    type = Column(CHAR(100), nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    
    detectlicense = relationship("DetectedLicense", back_populates="image")
    fromdataset = relationship("Dataset", back_populates="data")
    yololabel = relationship("YoloLabel", back_populates="fromimage")
    entryimage = relationship("ParkingData", back_populates="enimage", foreign_keys="ParkingData.entry_img")
    exitimage = relationship("ParkingData", back_populates="eximage", foreign_keys="ParkingData.exit_img")

    
class DetectedLicense(Base):
    __tablename__ = "detectedlicense"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    license_number = Column(CHAR(20), nullable=True)
    image_id = Column(Integer, ForeignKey("image.id"), nullable=False)
    
    image = relationship("Image", back_populates="detectlicense")

class Dataset(Base):
    __tablename__ = "dataset"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    dataset_name = Column(VARCHAR(100), nullable=False)
    
    data = relationship("Image", back_populates="fromdataset")
    
class YoloLabel(Base):
    __tablename__ = "yololabel"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    x_center = Column(Double, nullable=False)
    y_center = Column(Double, nullable=False)
    width = Column(Double, nullable=False)
    height = Column(Double, nullable=False)
    image_id = Column(Integer, ForeignKey("image.id"), nullable=False)

    fromimage = relationship("Image", back_populates="yololabel")
    
class ParkingData(Base):
    __tablename__ = "parkingdata"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    license = Column(CHAR(20), nullable=False)
    entry_img = Column(Integer, ForeignKey("image.id"), nullable=False)
    entry_time = Column(DATETIME, nullable=False)
    exit_img = Column(Integer, ForeignKey("image.id"))
    exit_time = Column(DATETIME)
    
    enimage = relationship("Image", back_populates="entryimage", foreign_keys=[entry_img])
    eximage = relationship("Image", back_populates="exitimage", foreign_keys=[exit_img])

    
class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    address = Column(VARCHAR(255))
    parking_id = Column(Integer, ForeignKey("parkingdata.id"), nullable=False)
    payment_amount = Column(Double, nullable=False)
    payment_time = Column(DATETIME, nullable=False)
    
class ParkingLot(Base):
    __tablename__ = "parkinglot"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    maxspace = Column(Integer, nullable = False)
    remainingspace = Column(Integer, nullable = False)
    
class Role(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(CHAR(10), nullable=False, unique=True)
    description = Column(VARCHAR(255))
    
    userRole = relationship("UserDetails", back_populates="userrole")
    
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = Column(CHAR(20), unique=True, nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    
    details = relationship("UserDetails", back_populates="userid")
    
class UserDetail(Base):
    __tablename__ = "userdetails"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True, unique=True, nullable=False)
    fullname = Column(VARCHAR(255), nullable=False)
    gender = Column(CHAR(10))
    phonenumber = Column(CHAR(15))
    balance = Column(Double)
    roleid = Column(Integer, ForeignKey("role.id"), nullable=False)
    
    userid = relationship("User", back_populates="details")
    userrole = relationship("Role", back_populates="userRole")
    
class TransactionDetail(Base):
    __tablename__ = "transactiondetails"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    userid = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    balancechanges = Column(Double)
    description = Column(VARCHAR(255))
    