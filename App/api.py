from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from licensedetection.LP_recognition import LP_recognition
from util import save_upload_file_tmp
import time
from fastapi.middleware.cors import CORSMiddleware
import json

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


@app.post("/detect")
def detect_license(img: UploadFile = File(...)):
    response = dict()
    start = time.time()
    tmp_path = save_upload_file_tmp(img)
    licensenum = LP_recognition(img_path=tmp_path)
    execution_time = time.time() - start
    time_string = "{}s".format(round(execution_time, 4))
    response["license_number"] = licensenum
    response["execution_time"] = time_string
    print(str(response))
    tmp_path.unlink()
    return JSONResponse(content=response)

