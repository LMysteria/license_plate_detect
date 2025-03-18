from fastapi import FastAPI, UploadFile, File, Path, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from .licensedetection.LP_recognition import LP_recognition
from . import util
import time
import os
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .database import models, connectdb, crud
from typing import Annotated
from datetime import datetime
from .auth import authcontroller, authcrud
from .schema import data
from .admin.admin import adminapi
from .router.user.user import userrouter

# Initiate database
models.Base.metadata.create_all(bind=connectdb.engine)

app = FastAPI(debug=True)

app.mount("/admin", adminapi)
app.include_router(userrouter)

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

@app.post("/signup", tags=["Auth"], response_model=data.User)
def signup(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return authcontroller.signup_user(username=username, password=password)

@app.post("/login", tags=["Auth"])
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]) -> data.Token:
    return await authcontroller.authenticate_user(username=username, password=password)

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

@app.get("/get/images/{type}", tags=["Get"])
def get_images_type(type: Annotated[str, Path()], offset: int = 0, limit: int = 100):
    return crud.get_images_byType(type=type, offset=offset, limit=limit)

@app.get("/get/yolo/dataset/{datasetid}/data/{type}", tags=["Get"])
def get_images_type(datasetid:Annotated[int, Path()], type: Annotated[str, Path()], offset: int = 0, limit: int = 100):
    data = crud.get_data_by_yolodataset_filtertype(type=type, offset=offset, limit=limit, dataset_id=datasetid)
    for i in range(len(data)):
        data[i] = {"image":data[i][0], "label":data[i][1]}
    return data


#Remove on production
@app.get("/role/details", tags=["User"])
def get_role_detail(roleid: int):
    return authcrud.get_role_access_by_roleid(id=roleid)

from .admin import adminutil

@app.put("/role/setrole", tags=["User"])
def set_role(username:Annotated[str, Form()], rolename: Annotated[str, Form()]):
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