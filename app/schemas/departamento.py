from sqlmodel import SQLModel

class DepartamentoCreate(SQLModel):
    nombre: str

class DepartamentoResponse(DepartamentoCreate):
    id: int

class DepartamentoUpdate(SQLModel):
    nombre: str | None = None
