from fastapi import FastAPI, Form
from typing import Annotated
from licensedetection.LP_recognition import LP_recognition
import time

app = FastAPI()

@app.post("/detect")
def detect_license(img_path: Annotated[str, Form()], img_ext: Annotated[str, Form()]):
    start = time.time()
    response = LP_recognition(img_path=img_path, img_ext=img_ext)
    execution_time = time.time() - start
    time_string = "{} s".format(round(execution_time, 4))
    response["execution_time"] = time_string
    return response