import datetime
from fastapi import FastAPI, HTTPException, Depends, status # type: ignore
from typing import Annotated # type: ignore
import models
from database import Base, SessionLocal, engine # type: ignore
from sqlalchemy.orm import Session # type: ignore
import uuid
from schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate, LoginCredentialsRequest, SedeCreate, SedeResponse, SedeUpdate, UserValidationResponse

models.Base.metadata.create_all(bind=engine)

# Crea una instancia de la aplicación FastAPI
app = FastAPI()


# Crea una base de datos de ejemplo
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Para inyeccion de dependencias:
db_dependency = Annotated[Session, Depends(get_db)]

#################### employee
@app.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: db_dependency):
    db_employee = models.Employees(**employee.dict(exclude_unset=True))
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def read_employee(employee_id: uuid.UUID, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.get("/employees", response_model=list[EmployeeResponse])
async def get_all_employees(db: db_dependency):
    db_employees = db.query(models.Employees).all()
    return db_employees

@app.get("/employees/{employee_id}/sede", response_model=SedeResponse)
async def get_sede_by_employee_id(employee_id: uuid.UUID, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.id == employee_id).first()

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db_sede = db_employee.sede
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")

    return db_sede

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: uuid.UUID, updated_data: EmployeeUpdate, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.id == employee_id).first()

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: uuid.UUID, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

############################ AUTH ############
#Endpoints para autenticacion
@app.post("/employees/credentials", response_model=UserValidationResponse)
async def login_employee(employee: LoginCredentialsRequest, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.email == employee.email).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return UserValidationResponse(
        userId=db_employee.id,
        email=db_employee.email,
        hashedPassword=db_employee.password,
        roles= ["ROLE_EMPLOYEE"]
    )


######################################## SEDE ##########################################

@app.post("/sede", response_model=SedeResponse, status_code=status.HTTP_201_CREATED)
async def create_sede(sede: SedeCreate, db: db_dependency):
    db_sede = models.Sede(**sede.dict())
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede

@app.get("/sede/{sede_id}", response_model=SedeResponse)
async def read_sede(sede_id: uuid.UUID, db: db_dependency):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")
    return db_sede

@app.get("/sede", response_model=list[SedeResponse])
async def get_all_sedes(db: db_dependency):
    sedes = db.query(models.Sede).all()
    return sedes

@app.get("/sede/{sede_id}/employees", response_model=list[EmployeeResponse])
async def get_employees_by_sede_id(sede_id: uuid.UUID, db: db_dependency):
    sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")

    employees = db.query(models.Employees).filter(models.Employees.sede_id == sede_id).all()
    return employees

@app.put("/sede/{sede_id}", response_model=SedeResponse)
async def update_sede(sede_id: uuid.UUID, updated_data: SedeUpdate, db: db_dependency):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()

    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_sede, key, value)

    db.commit()
    db.refresh(db_sede)
    return db_sede

@app.delete("/sede/{sede_id}", status_code=status.HTTP_200_OK)
async def delete_employee(sede_id: uuid.UUID, db: db_dependency):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")
    db.delete(db_sede)
    db.commit()
    return {"message": "Sede deleted successfully"}

