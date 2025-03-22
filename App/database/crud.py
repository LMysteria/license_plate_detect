from . import connectdb, models
from typing import Annotated
from datetime import datetime
import time
from sqlalchemy.sql.functions import now


def get_image_byID(image_id: int) -> models.Image:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.Image).filter(models.Image.id == image_id).first()
        
        print("Get Image ByID SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_image_by_path(path: str, datasetname: Annotated[str, None] = None) -> models.Image:
    with connectdb.session() as db:
        if datasetname:
            dbdataset = get_dataset_by_datasetname(datasetname)
            if not dbdataset:
                create_dataset(dataset_name=datasetname)
            response = db.query(models.Image).filter(models.Image.path == path, 
                                                 models.Image.dataset_id == dbdataset.id).first()
            
        else:
            response = db.query(models.Image).filter(models.Image.path == path).first()
            
        return response
    
def get_license_byID(license_id: int) -> models.DetectedLicense:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.DetectedLicense).filter(models.DetectedLicense.id == license_id).first()
        
        print("Get License ByID SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_dataset_byID(dataset_id: int) -> models.Dataset:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    
        print("Get Dataset byID SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_dataset_by_datasetname(dataset_name: str) -> models.Dataset:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.Dataset).filter(models.Dataset.dataset_name == dataset_name).first()
    
        print("Get Dataset byDatasetname SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_images_byDataset(dataset_id: int, offset: int = 0, limit: int = 100) -> list[models.Image]:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.Image).filter(models.Image.dataset_id == dataset_id).offset(offset).limit(limit).all()

        print("Get Images byDataset SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_license_byImage(image_id: int) -> list[models.DetectedLicense]:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.DetectedLicense).filter(models.DetectedLicense.image_id == image_id).all()
        
        print("Get License byImage SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_data_by_dataset(dataset_id: int, offset: int = 0, limit: int = 100) -> list:
    start = time.time()

    with connectdb.session() as db:
        img_license_set = list()
        images = get_images_byDataset(dataset_id, offset, limit)
        for img in images:
            licenses = get_license_byImage(img.id)
            img_license_set.append({"image":img, "detectedlicense":licenses}) 
            
        print("Get Data byDataset SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return img_license_set
    
def get_data_by_yolodataset_filtertype(dataset_id: int,type: str, offset: int = 0, limit: int = 100) -> list:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.Image, models.YoloLabel).filter(models.Image.dataset_id==dataset_id).filter(
                                                        models.Image.type == type).filter(
                                                        models.YoloLabel.image_id == models.Image.id).offset(offset=offset).limit(limit=limit).all()
        print("Get Data byDataset SQL Execution time: {}s".format(round(time.time()-start, 4)))
        print(response)
        return response
    
def get_datasets(offset: int = 0, limit: int = 100) -> list[models.Dataset]:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.Dataset).offset(offset).limit(limit).all()
    
        print("Get Datasets SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_images(offset: int = 0, limit: int = 100) -> list[models.Image]:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.Image).offset(offset).limit(limit).all()
        
        print("Get Images SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_images_byType(type: str, offset: int = 0, limit: int = 100) -> list[models.Image]:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.Image).filter(models.Image.type == type).offset(offset).limit(limit).all()
        
        print("Get Images byType SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_detectedlicenses(offset: int = 0, limit: int = 100) -> list[models.DetectedLicense]:
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.DetectedLicense).offset(offset).limit(limit).all()
        
        print("Get Licenses SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_data_by_dataset_sql(dataset_id: int, offset: int = 0, limit: int = 100):
    start = time.time()

    with connectdb.session() as db:
        sql = 'SELECT * FROM image, detectedlicense where image.id=detectedlicense.image_id and image.dataset_id = {} LIMIT {} OFFSET'.format(dataset_id, limit, offset)
        response = db.execute(sql)
        
        print("Get Data ByDataset raw SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    
def get_last_parkingdata_by_licensenumber(licensenumber: str, parkingareaid:int):
    start = time.time()

    with connectdb.session() as db:
        response = db.query(models.ParkingData).filter(models.ParkingData.license == licensenumber and 
                                                       models.ParkingData.parkingareaid==parkingareaid).order_by(models.ParkingData.id.desc()).first()
        
        print("Get last parkingdata by licensenumber SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return response
    

#CREATE
def create_image(image_path: str, type: str, dataset_id: Annotated[int, None] = None) -> models.Image:
    start = time.time()

    with connectdb.session() as db:
        if dataset_id and not get_dataset_byID(dataset_id=dataset_id):
            raise Exception("Dataset not Found")
        db_image = models.Image(path=image_path, dataset_id=dataset_id, type = type)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        print("Create Image SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return db_image
        
def create_detectedlicense(license_number: str, image_id: int) -> models.DetectedLicense:
    start = time.time()

    with connectdb.session() as db:
        db_detectedlicense = models.DetectedLicense(license_number=license_number, image_id=image_id)
        db.add(db_detectedlicense)
        db.commit()
        db.refresh(db_detectedlicense)
        
        print("Create DetectLicense SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return db_detectedlicense
    
def create_dataset(dataset_name: str) -> models.Dataset:
    start = time.time()

    with connectdb.session() as db:
        db_dataset = models.Dataset(dataset_name=dataset_name)
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        
        print("Create Dataset SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return db_dataset
    
def parking_entry(license_number:str, entry_image_id: int, parkingareaid:int):
    start = time.time()

    with connectdb.session() as db:
        dbparkingdata = models.ParkingData(license=license_number, entry_img=entry_image_id, entry_time=now(), parkingareaid=parkingareaid)
        db.add(dbparkingdata)
        db.commit()
        db.refresh(dbparkingdata)

        print("Create ParkingData SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return dbparkingdata
            
def bulk_create_image(list_image: list[dict]):
    start = time.time()

    try:
        with connectdb.session() as db:
            images = []
            for imgdict in list_image:
                images.append(models.Image(path=imgdict["path"], dataset_id=imgdict["dataset_id"], type=imgdict["type"]))
            db.bulk_save_objects(images)
            db.commit()
            
            print("Bulk Create Image SQL Execution time: {}s".format(round(time.time()-start, 4)))
            return True
    except:
        return False
    
def bulk_create_license(list_detectedlicense: list[dict]):
    start = time.time()

    try:
        with connectdb.session() as db:
            detectedlicenses = []
            for licensedict in list_detectedlicense:
                detectedlicenses.append(models.DetectedLicense(license_number=licensedict["license_number"], image_id=licensedict["image_id"]))
            db.bulk_save_objects(detectedlicenses)
            db.commit()
            
            print("Bulk Create license SQL Execution time: {}s".format(round(time.time()-start, 4)))
            return True
    except:
        return False
    
def bulk_create_yololabel(list_yolov5label: list[dict]):
    start = time.time()

    try:
        with connectdb.session() as db:
            yolov5labels = []
            for labeldict in list_yolov5label:
                yolov5labels.append(models.YoloLabel(x_center=labeldict["x_center"], y_center=labeldict["y_center"], 
                                                       width=labeldict["width"], height=labeldict["height"], image_id=labeldict["image_id"]))
            db.bulk_save_objects(yolov5labels)
            db.commit()
            
            print("Bulk create yololabel SQL Execution time: {}s".format(round(time.time()-start, 4)))
            return True
        
    except:
        return False        
    
#UPDATE
def parking_exit(license_number:str, exit_image: models.Image, parkingareaid:int):
    start = time.time()

    with connectdb.session() as db:
        dbparkingdata = get_last_parkingdata_by_licensenumber(licensenumber=license_number, parkingareaid=parkingareaid)
        dbparkingdata.eximage=exit_image
        dbparkingdata.exit_time = now()
        db.add(dbparkingdata)
        db.commit()
        db.refresh(dbparkingdata)
        
        print("Parking Data Update SQL Execution time: {}s".format(round(time.time()-start, 4)))
        return dbparkingdata