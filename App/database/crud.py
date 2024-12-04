from . import connectdb, models
from typing import Annotated

def get_image_byID(image_id: int) -> models.Image:
    with connectdb.session() as db:
        return db.query(models.Image).filter(models.Image.id == image_id).first()
    
def get_image_by_path(path: str, datasetname: Annotated[str, None] = None) -> models.Image:
    with connectdb.session() as db:
        if datasetname:
            dbdataset = get_dataset_by_datasetname(datasetname)
            if not dbdataset:
                create_dataset(dataset_name=datasetname)
            return db.query(models.Image).filter(models.Image.path == path, 
                                                 models.Image.dataset_id == dbdataset.id).first()
        return db.query(models.Image).filter(models.Image.path == path).first()
    
def get_license_byID(license_id: int) -> models.DetectedLicense:
    with connectdb.session() as db:
        return db.query(models.DetectedLicense).filter(models.DetectedLicense.id == license_id).first()
    
def get_dataset_byID(dataset_id: int) -> models.Dataset:
    with connectdb.session() as db:
        return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    
def get_dataset_by_datasetname(dataset_name: str) -> models.Dataset:
    with connectdb.session() as db:
        return db.query(models.Dataset).filter(models.Dataset.dataset_name == dataset_name).first()
    
def get_images_byDataset(dataset_id: int, offset: int = 0, limit: int = 100) -> list[models.Image]:
    with connectdb.session() as db:
        return db.query(models.Image).filter(models.Image.dataset_id == dataset_id).offset(offset).limit(limit).all()
    
def get_license_byImage(image_id: int) -> list[models.DetectedLicense]:
    with connectdb.session() as db:
        return db.query(models.DetectedLicense).filter(models.DetectedLicense.image_id == image_id).all()
    
def get_data_by_dataset(dataset_id: int, offset: int = 0, limit: int = 100) -> list:
    with connectdb.session() as db:
        img_license_set = list()
        images = get_images_byDataset(dataset_id, offset, limit)
        for img in images:
            licenses = get_license_byImage(img.id)
            img_license_set.append({"image":img, "detectedlicense":licenses}) 
        return img_license_set
    
def get_datasets(offset: int = 0, limit: int = 100) -> list[models.Dataset]:
    with connectdb.session() as db:
        return db.query(models.Dataset).offset(offset).limit(limit).all()
    
def get_images(offset: int = 0, limit: int = 100) -> list[models.Image]:
    with connectdb.session() as db:
        return db.query(models.Image).offset(offset).limit(limit).all()
    
def get_detectedlicenses(offset: int = 0, limit: int = 100) -> list[models.DetectedLicense]:
    with connectdb.session() as db:
        return db.query(models.DetectedLicense).offset(offset).limit(limit).all()
    
def get_data_by_dataset_sql(dataset_id: int, offset: int = 0, limit: int = 100):
    with connectdb.session() as db:
        sql = 'SELECT * FROM image, detectedlicense where image.id=detectedlicense.image_id and image.dataset_id = {} LIMIT {} OFFSET'.format(dataset_id, limit, offset)
        return db.execute(sql)
    
#CREATE
def create_image(image_path: str, type: str, dataset_id: Annotated[int, None] = None) -> models.Image:
    with connectdb.session() as db:
        if dataset_id and not get_dataset_byID(dataset_id=dataset_id):
            raise Exception("Dataset not Found")
        db_image = models.Image(path=image_path, dataset_id=dataset_id, type = type)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
        
def create_detectedlicense(license_number: str, image_id: int) -> models.DetectedLicense:
    with connectdb.session() as db:
        db_detectedlicense = models.DetectedLicense(license_number=license_number, image_id=image_id)
        db.add(db_detectedlicense)
        db.commit()
        db.refresh(db_detectedlicense)
        return db_detectedlicense
    
def create_dataset(dataset_name: str) -> models.Dataset:
    with connectdb.session() as db:
        db_dataset = models.Dataset(dataset_name=dataset_name)
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        return db_dataset
    
def bulk_create_image(list_image: list[dict]):
    try:
        with connectdb.session() as db:
            images = []
            for imgdict in list_image:
                images.append(models.Image(path=imgdict["path"], dataset_id=imgdict["dataset_id"], type=imgdict["type"]))
            db.bulk_save_objects(images)
            db.commit()
            return True
    except:
        return False
    
def bulk_create_license(list_detectedlicense: list[dict]):
    try:
        with connectdb.session() as db:
            detectedlicenses = []
            for licensedict in list_detectedlicense:
                detectedlicenses.append(models.DetectedLicense(license_number=licensedict["license_number"], image_id=licensedict["image_id"]))
            db.bulk_save_objects(detectedlicenses)
            db.commit()
            return True
    except:
        return False
    
def bulk_create_yolov5label(list_yolov5label: list[dict]):
    try:
        with connectdb.session() as db:
            yolov5labels = []
            for labeldict in list_yolov5label:
                yolov5labels.append(models.Yolov5Label(x_center=labeldict["x_center"], y_center=labeldict["y_center"], 
                                                       width=labeldict["width"], height=labeldict["height"], image_id=labeldict["image_id"]))
            db.bulk_save_objects(yolov5labels)
            db.commit()
    except:
        return False        