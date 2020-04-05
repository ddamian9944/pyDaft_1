from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
app.counter = 0
app.patients = {}

class MessageResp(BaseModel):
    message: str

@app.get("/", response_model=MessageResp)
def root():
    return MessageResp(message="Hello World during the coronavirus pandemic!")

class MethodResp(BaseModel):
    method: str

@app.get("/method")
def return_get_response():
    return MethodResp(method="GET")

@app.post("/method", response_model=MethodResp)
def return_post_response():
    return MethodResp(method="POST")

@app.put("/method", response_model=MethodResp)
def return_put_response():
    return MethodResp(method="PUT")

@app.delete("/method", response_model=MethodResp)
def return_delete_response():
    return MethodResp(method="DELETE")

class AddNewPatient(BaseModel):
    name: str
    surename: str


class ReturnPatient(BaseModel):
    id: int = app.counter
    patient: Dict


@app.post("/patient", response_model=ReturnPatient)
def add_patient(patient_info: AddNewPatient):
    _id = app.counter
    app.patients[_id] = patient_info.dict()
    counter()
    return ReturnPatient(id=_id, patient=patient_info.dict())


@app.get("/patient/{pk}")
def find_patient(pk: int):
    if pk not in app.patients.keys():
        raise HTTPException(
            status_code=204,
            detail="Patient with this id not found.")
    return app.patients[pk]
