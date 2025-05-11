from datetime import datetime
from sqlalchemy import Column, DateTime, String, Float, ForeignKey
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import enum  # Importamos enum de Python
from sqlalchemy.types import Uuid # Import Uuid type
from database import Base
from sqlalchemy import Column, DateTime
from datetime import datetime

# Definimos el Enum de Python
class RoleEnum(str, enum.Enum):
    TRAINER = "Trainer"
    NUTRICIONIST = "Nutricionist"
    ADMINISTRATOR = "Administrator"


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50))
    lastName = Column(String(50))
    age = Column(Float)
    phone = Column(String(20))
    email = Column(String(50))
    password = Column(String(72))
    imagenUrlKey = Column(String(100))
    salary = Column(Float)
    dateContract = Column(DateTime, default=datetime.utcnow)

    role = Column(String(15), default=RoleEnum.TRAINER, nullable=False)

    sedeId = Column(Uuid, ForeignKey('sede.id'), nullable=False)
    sede = relationship("Sede", back_populates="employees")


class Sede(Base):
    __tablename__ = 'sede'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50))
    address = Column(String(50))
    phone = Column(String(50))
    imagenUrlKey = Column(String(100))

    employees = relationship("Employees", back_populates="sede", cascade="all, delete-orphan")    