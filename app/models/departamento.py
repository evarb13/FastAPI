from sqlmodel import SQLModel, Field, Relationship

class Departamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str | None = None

    empleados: list["Empleado"] = Relationship(back_populates="departamento", cascade_delete=True)