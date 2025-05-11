from typing import List
from pydantic import BaseModel, EmailStr # type: ignore
from models import RoleEnum
import uuid
from datetime import datetime

# Define un modelo Pydantic para la validación de datos
class EmployeeCreate(BaseModel):
    name: str
    lastName: str
    age: int
    phone: str
    email: str
    password: str
    imagenUrlKey: str | None = None
    salary: float | None = None
    role: RoleEnum | None = None
    sedeId: uuid.UUID

class EmployeeUpdate(BaseModel):
    name: str | None = None
    lastName: str | None = None
    age: int | None = None
    phone: str | None = None
    email: str | None = None
    password: str | None = None
    imagenUrlKey: str | None = None
    salary: float | None = None
    role: RoleEnum | None = None
    sedeId: uuid.UUID | None = None

    class Config:
        orm_mode = True

# Modelo de respuesta (incluye campos generados como id y fecha de contrato)
class EmployeeResponse(BaseModel):
    id: uuid.UUID
    name: str
    lastName: str | None = None
    age: int
    phone: str
    email: str
    imagenUrlKey: str | None = None
    salary: float | None = None
    role: RoleEnum = RoleEnum.TRAINER
    sedeId: uuid.UUID
    dateContract: datetime

    class Config:
        orm_mode = True

#################### SEDE ######################

class SedeCreate(BaseModel):
    name: str
    address: str | None = None
    phone: str
    imagenUrlKey: str | None = None

class SedeUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    imagenUrlKey: str | None = None

    class Config:
        orm_mode = True

class SedeResponse(SedeCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True


################### SECURITY ##################
class LoginCredentialsRequest(BaseModel):
    email: EmailStr
    password: str # Contraseña en texto plano para validar
    userType: str | None = None # Tipo de usuario (opcional)

class UserValidationResponse(BaseModel): # Respuesta para AuthService
    userId: uuid.UUID
    email: EmailStr
    hashedPassword: str
    roles: List[str]