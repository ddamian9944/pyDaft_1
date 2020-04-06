from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
counter: int = 0
patients = []

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

class AddPatientRq(BaseModel):
    name: str
    surename: str


class AddPatientResp(BaseModel):
    id: int
    patient: AddPatientRq


@app.post('/patient')
def add_patient(patient: AddPatientRq):
    global counter, patients

    patient = AddPatientResp(id=counter, patient=patient)
    patients.append(patient)
    counter += 1
    return patient


@app.get('/patient/{pk}')
def get_patient(pk: int):
    global patients

    patient_resp = next((patient for patient in patients if patient.id == pk), None)
    if patient_resp:
        return patient_resp.patient
    else:
        return JSONResponse(status_code=204, content={})