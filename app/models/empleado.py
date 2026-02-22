from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Empleado(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    puesto: str
    imagen_uri: str | None = None
    departamento_id: int = Field(foreign_key="departamento.id")

    departamento: Optional["Departamento"] = Relationship(back_populates="empleados")