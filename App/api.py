from fastapi import FastAPI, UploadFile, File, Path
from fastapi.responses import JSONResponse
from licensedetection.LP_recognition import LP_recognition
import util
import time
import os
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from database import models, connectdb, crud
import glob
from typing import Annotated

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
    dbimage = crud.create_image(relpath, type="val")
    for license in detected:
        crud.create_detectedlicense(license_number=license, image_id=dbimage.id)
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    response["license_number"] = detected
    response["execution_time"] = time_string
    print(str(response))
    return JSONResponse(content=response)

#CREATE
@app.post("/create/dataset", tags=["Create"])
def create_dataset(dataset_name: str):
    return crud.create_dataset(dataset_name=dataset_name)

@app.post("/bulk/create/image", tags=["Create"])
def bulk_create_image(type: str = "val", images: list[UploadFile] = File(...), dataset_id: Annotated[int, None] = None):
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
    return crud.bulk_create_image(create_images)

@app.post("/bulk/create/dataset/yolov5", tags=["Create"])
def bulk_create_dataset_yolov5(dataset_name: str, zipfile: UploadFile = File(...)):
    response = util.import_yolov5_dataset(file=zipfile, datasetname=dataset_name)
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