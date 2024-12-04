from sqlalchemy import Column, Integer, CHAR, ForeignKey, VARCHAR, Double
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
    yolov5label = relationship("Yolov5Label", back_populates="fromimage")

    
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
    
class Yolov5Label(Base):
    __tablename__ = "yolov5label"
    id = id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    x_center = Column(Double, nullable=False)
    y_center = Column(Double, nullable=False)
    width = Column(Double, nullable=False)
    height = Column(Double, nullable=False)
    image_id = Column(Integer, ForeignKey("image.id"), nullable=False)

    fromimage = relationship("Image", back_populates="yolov5label")