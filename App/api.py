from fastapi import FastAPI, UploadFile, File, Path
from fastapi.responses import JSONResponse
from licensedetection.LP_recognition import LP_recognition
import util
import time
import os
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from database import models, connectdb, crud
from typing import Annotated
from datetime import datetime

# Initiate database
models.Base.metadata.create_all(bind=connectdb.engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/detect", tags=["License Detection AI"])
def detect_license(img: UploadFile = File(...)):
    response = dict()
    start = time.time()
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    for license in detected:
        crud.create_detectedlicense(license_number=license, image_id=dbimage.id)
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    response["license_number"] = detected
    response["execution_time"] = time_string
    print(str(response))
    return JSONResponse(content=response)

@app.post("/parking/entry", tags=["Parking"])
def parking_entry(img: UploadFile):
    response = dict()
    start = time.time()
    
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_entry(license_number=licensedb.license_number, entry_image_id=dbimage.id, entry_datetime=datetime.now())
    
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    response["parkingdata"] = parkingdb
    response["execution_time"] = time_string
    return response

@app.post("/parking/exit", tags=["Parking"])
def parking_exit(img: UploadFile):
    response = dict()
    start = time.time()
    
    relpath = os.path.join("uploadfile", img.filename)
    fullpath = os.path.join(os.getcwd(),relpath)
    util.save_upload_file(img, Path(fullpath))
    detected = LP_recognition(img_path=relpath)
    dbimage = crud.create_image(relpath, type="detect")
    licensedb = crud.create_detectedlicense(license_number=detected[0], image_id=dbimage.id)
    parkingdb = crud.parking_exit(license_number=licensedb.license_number, exit_image=dbimage, exit_datetime=datetime.now())
    
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    response["parkingdata"] = parkingdb
    response["execution_time"] = time_string
    return response

#CREATE
@app.post("/create/dataset", tags=["Create"])
def create_dataset(dataset_name: str):
    return crud.create_dataset(dataset_name=dataset_name)

@app.post("/bulk/create/image", tags=["Create"])
def bulk_create_image(type: str = "val", images: list[UploadFile] = File(...), dataset_id: Annotated[int, None] = None):
    start = time.time()
    create_images: list[dict] = list()
    for img in images:
        if dataset_id:
            dbdataset = crud.get_dataset_byID(dataset_id=dataset_id)
            Path(os.path.join(os.getcwd(),"dataset",dbdataset.dataset_name)).mkdir(exist_ok=True)

            relpath = os.path.join("dataset",dbdataset.dataset_name, img.filename)
        else:
            relpath = os.path.join("uploadfile", img.filename)
        fullpath = os.path.join(os.getcwd(),relpath)
        util.save_upload_file(img, Path(fullpath))
        create_images.append({"path":relpath, "dataset_id":dataset_id, "type":type})

    response = crud.bulk_create_image(create_images)
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    print("bulk create images execution time: ",time_string)
    return response

@app.post("/bulk/create/dataset/yolo", tags=["Create"])
def bulk_create_dataset_yolo(dataset_name: str, zipfile: UploadFile = File(...)):
    """ import yolo dataset

    please name your yaml file data.yaml
    
    Args:
        dataset_name (str): dataset name
        zipfile (UploadFile): yolo dataset zipfile

    Returns:
        Boolean: True for successful, False for failure
    """
    start = time.time()
    response = util.import_yolo_dataset(file=zipfile, datasetname=dataset_name)
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    print("Import yolo dataset execution time: ",time_string)
    return response
    
#GET
@app.get("/get/dataset/{dataset_id}", tags=["Get"])
def get_dataset(dataset_id: Annotated[int, Path()]):
    return crud.get_dataset_byID(dataset_id=dataset_id)

@app.get("/get/image/{image_id}", tags=["Get"])
def get_dataset(image_id: Annotated[int, Path()]):
    return crud.get_image_byID(image_id=image_id)

@app.get("/get/detectedlicense/{license_id}", tags=["Get"])
def get_dataset(license_id: Annotated[int, Path()]):
    return crud.get_license_byID(license_id=license_id)

@app.get("/get/datasets", tags=["Get"])
def get_dataset(offset: int = 0, limit: int = 100):
    return crud.get_datasets(offset=offset, limit=limit)

@app.get("/get/images", tags=["Get"])
def get_dataset(offset: int = 0, limit: int = 100):
    return crud.get_images(offset=offset, limit=limit)

@app.get("/get/detectedlicenses", tags=["Get"])
def get_dataset(offset: int = 0, limit: int = 100):
    return crud.get_detectedlicenses(offset=offset, limit=limit)