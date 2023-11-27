# dataAPI


## Project structure:


```
dataAPI/
 |-- app/
 |   |-- common/ 
 |   |-- data/
 |   |-- schemas/
 |   |-- service/
 |   |-- main.py ( main file)
 |   |-- Dockerfile
 |   |-- requirements.txt
 |-- cdk/
 |   |-- cdk.json 
 |   |-- cdk.py 
 |   |-- fastapi_stack.py
 |-- SQL/
 |   |-- ex1.sql 
 |   |-- ex2.sql 
```

## Infraestructure


To create image locally, standing on app folder, run 

```
docker build -t data-app .
docker tag data-app:latest public.ecr.aws/h6v8e9c5/data-app:latest
docker push public.ecr.aws/h6v8e9c5/data-app:latest
```

To create infraestructure on aws, standing on cdk folder run
```
cdk bootstrap
cdk deploy
```

To clean 
```
cdk destroy FastAPIStack
```

## API

Python application using FastAPI layer architecture employing pagackes: common, schemas, and services; additionally, the data folder contains the CSV files.

## SQL
The two sql files that satisfy the requirements are located inside the SQL folder.
