from fastapi import FastAPI
from schemas.request import FileName
from service.files import Jobs, Departments, HiredEmployees

app = FastAPI()


@app.get("/")
def get_root():
    return {"message": "DataAPI using FastAPI"}


@app.post("/update/")
def update(fl: FileName):
    match fl.value:
        case 'job':
            return Jobs.upload_data()
        case 'departments':
            return Departments.upload_data()
        case 'hired_employees':
            return HiredEmployees.upload_data()

@app.get("/data/")
def get_user(fl: FileName, pg: int = 1):
    match fl.value:
        case 'job':
            return Jobs.get_data(pg)
        case 'departments':
            return Departments.get_data(pg)
        case 'hired_employees':
            return HiredEmployees.get_data(pg)


#DATABASE="dev_database" USER_NAME="deuser" PASSWORD="depasswd" HOST="localhost" uvicorn main:app --reload

#cdk bootstrap
#cdk deploy