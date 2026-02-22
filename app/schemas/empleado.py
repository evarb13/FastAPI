from sqlmodel import SQLModel

# Para añadir un empleado
class EmpleadoCreate(SQLModel):
    nombre: str
    apellido: str
    departamento_id: int
    puesto: str | None = None
    imagen_uri: str | None = None

# Para cuando quiero mostrar el empleado
class EmpleadoResponse(EmpleadoCreate):
    id: int

# Para cuando quiero actualizar, por eso todos los campos son opcionales
class EmpleadoUpdate(SQLModel):
    nombre: str | None = None
    apellido: str | None = None
    puesto: str | None = None
    imagen_uri: str | None = None
    departamento_id: int | None = None


# Es importante que si hay un dato que no queremos que se vea en el Response tenfriamos que haceruna clase base.
# Y luego otras dos que heredarian de esta pero en la del create, que es improtante que este salario
# puedas guardar todos los datos y en el response loq ue queremos mostrar que seria lo mismo que la base + el id.
# veremos que tambien se puede excluir un campo desde los routers sin tener que hacerlo desde aqui.
# 1. Lo que todo el mundo puede ver
#class EmpleadoBase(SQLModel):
#    nombre: str
#    puesto: str

# 2. Para crear (Añadimos el salario)
#class EmpleadoCreate(EmpleadoBase):
#    salario: float

# 3. Para responder (Añadimos el ID, pero NO hereda el salario)
#class EmpleadoResponse(EmpleadoBase):
#    id: int