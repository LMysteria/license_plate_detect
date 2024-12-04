import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
import os
import zipfile
import glob
from fastapi import UploadFile
from database import crud


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def import_yolov5_dataset(file: UploadFile, datasetname: str):
    dbdataset = crud.get_dataset_by_datasetname(dataset_name=datasetname)

    path = os.path.join(os.getcwd(),"dataset",datasetname)
    Path(path).mkdir(exist_ok=True)
    print("extracting zipfile")
    
    zippath = save_upload_file_tmp(file)
    
    with zipfile.ZipFile(zippath) as zip_file:
        print(f"files in zip: {zip_file.namelist()}")
        zip_file.extractall(path)

    if(not dbdataset):
        dbdataset = crud.create_dataset(dataset_name=datasetname)
    
    print("importing train images")
    dbvalimage: list[dict] = list()
    print(os.path.join(path,"images","val","*.png"))
    for valimage in glob.glob(os.path.join(path,"images","val","*.png")):
        valimage = valimage.split("\\")[-1]
        relpath = os.path.join("dataset", datasetname,"images","val",valimage)
        dbvalimage.append({"path":relpath, "dataset_id":dbdataset.id, "type":"val"})
    crud.bulk_create_image(dbvalimage)
    print("Imported val images")
    
    dbvallabel: list[dict] = list()
    Path(os.path.join(path,"labels","val")).mkdir(exist_ok=True)    
    for vallabel in glob.glob(os.path.join(path,"labels","val","*.txt")):
        vallabel = vallabel.split("\\")[-1]
        with open(os.path.join(path,"labels","val", vallabel), 'r') as readlabel:
            values = readlabel.read().split()
            relpath = os.path.join("dataset", datasetname,"images","val",vallabel.split('.')[0]+".png")
            dbimg = crud.get_image_by_path(relpath)
            for i in range((len(values)-1)//4):
                dbvallabel.append({"x_center":values[i*4+1], "y_center":values[i*4+2], "width":values[i*4+3], "height":values[i*4+4], "image_id":dbimg.id})
                
    crud.bulk_create_yolov5label(dbvalimage)
    print("Imported val labels")

    dbtrainimage: list[dict] = list()     
    for trainimage in glob.glob(os.path.join(path,"images","train","*.png")):
        trainimage = trainimage.split("\\")[-1]
        relpath = os.path.join("dataset", datasetname,"images","train",trainimage)
        dbtrainimage.append({"path":relpath, "dataset_id":dbdataset.id, "type":"train"})
    crud.bulk_create_image(dbtrainimage)
    print("Imported train images")
                
    dbtrainlabel: list[dict] = list()
    Path(os.path.join(path,"labels","train")).mkdir(exist_ok=True)    
    for trainlabel in glob.glob(os.path.join(path,"labels","train","*.txt")):
        trainlabel = trainlabel.split("\\")[-1]
        with open(os.path.join(path,"labels","train", trainlabel), 'r') as readlabel:
            values = readlabel.read().split()
            relpath = os.path.join("dataset", datasetname,"images","train",trainlabel.split('.')[0]+".png")
            dbimg = crud.get_image_by_path(relpath)
            for i in range((len(values)-1)//4):
                dbtrainlabel.append({"x_center":values[i*4+1], "y_center":values[i*4+2], "width":values[i*4+3], "height":values[i*4+4], "image_id":dbimg.id})
    crud.bulk_create_yolov5label(dbtrainlabel)
    print("Imported train labels")

            
    return True
