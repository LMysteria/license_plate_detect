import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
import os
import zipfile
import glob
from fastapi import UploadFile
from database import crud, models
import yaml

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
        
def import_yolo_dataset_image(dbdataset: models.Dataset, type: str, imgdirpath: str):
    print("importing {} images".format(type))
    dbimage: list[dict] = list()
    dbpath = os.path.join(os.getcwd(),"dataset",dbdataset.dataset_name)
    exttype = (".jpg",".png")
    for ext in exttype:
        for image in glob.glob(os.path.join(dbpath,imgdirpath,"*"+ext)):
            image = image.split("\\")[-1]
            relpath = "dataset\\{}\\{}\\{}".format(dbdataset.dataset_name, imgdirpath, image)
            dbimage.append({"path":relpath, "dataset_id":dbdataset.id, "type":type})
    crud.bulk_create_image(dbimage)    
    print("Imported {} images".format(type))
    
def import_yolo_dataset_label(dbdataset: models.Dataset, type:str,  imgdirpath: str):
    print("Importing {} labels".format(type))
    lbldirpath=imgdirpath.replace("images","labels")
    dblabel: list[dict] = list()
    dbpath = os.path.join(os.getcwd(),"dataset",dbdataset.dataset_name)
    for label in glob.glob(os.path.join(dbpath,lbldirpath,"*.txt")):
        label = label.split("\\")[-1]
        with open(os.path.join(dbpath, lbldirpath, label), 'r') as readlabel:
            values = readlabel.read().split()
            exttype = (".jpg",".png")
            for ext in exttype:
                imgrelpath = os.path.join("dataset", dbdataset.dataset_name,imgdirpath,label.replace(".txt",ext))
                dbimg = crud.get_image_by_path(imgrelpath)
                if dbimg:
                    break
            for i in range((len(values)-1)//4):
                dblabel.append({"x_center":values[i*4+1], "y_center":values[i*4+2], "width":values[i*4+3], "height":values[i*4+4], "image_id":dbimg.id})
                
    crud.bulk_create_yololabel(dblabel)
    print("Imported {} labels".format(type))
    

def import_yolo_dataset(file: UploadFile, datasetname: str):
    print("Importing dataset {}".format, datasetname)
    dbdataset = crud.get_dataset_by_datasetname(dataset_name=datasetname)

    path = os.path.join(os.getcwd(),"dataset",datasetname)
    Path(path).mkdir(exist_ok=True)
    print("Extracting zipfile")
    
    zippath = save_upload_file_tmp(file)
    
    with zipfile.ZipFile(zippath) as zip_file:
        print(f"files in zip: {zip_file.namelist()}")
        zip_file.extractall(path)

    print("Zipfile extracted")
        
    if(not dbdataset):
        dbdataset = crud.create_dataset(dataset_name=datasetname)
    
    
    with open(os.path.join(path,"data.yaml")) as stream:
        yamldata = yaml.safe_load(stream)
    trainpath = yamldata["train"].replace("../","").replace("/","\\")
    print(trainpath)
    
    
    import_yolo_dataset_image(dbdataset=dbdataset, type="train", imgdirpath = trainpath)
    import_yolo_dataset_label(dbdataset=dbdataset, type="train", imgdirpath = trainpath)
    
    if "val" in yamldata:
        valpath = yamldata["val"].replace("../","").replace("/","\\")
        import_yolo_dataset_image(dbdataset=dbdataset, type="val", imgdirpath = valpath)
        import_yolo_dataset_label(dbdataset=dbdataset, type="val", imgdirpath = valpath)
        
    if "test" in yamldata:
        testpath = yamldata["test"].replace("../","").replace("/","\\")
        import_yolo_dataset_image(dbdataset=dbdataset, type="test", imgdirpath = testpath)
        import_yolo_dataset_label(dbdataset=dbdataset, type="test", imgdirpath = testpath)
        
    print("Imported dataset {}".format(datasetname))
  
    return True
