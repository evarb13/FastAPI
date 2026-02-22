from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.models.empleado import Empleado
from app.db.session import get_session
from app.schemas.empleado import EmpleadoCreate, EmpleadoResponse, EmpleadoUpdate
import os
import shutil
from fastapi import UploadFile

class EmpleadoService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, empleado_data: EmpleadoCreate) -> EmpleadoResponse:
        empleado = Empleado(**empleado_data.model_dump()) # convierte el esquema en un diccionario normal de python
        self.session.add(empleado) # como el push de github (pone el objeto en la bandeja de salida)
        self.session.commit() # como el commit de github
        self.session.refresh(empleado) # para que se actualice en memoria el objeto
        return EmpleadoResponse(**empleado.model_dump())

    #Busca empleados aplicando filtros opcionales. Si no se pasan parámetros, devuelve la lista completa.
    def get_all(self, id: int | None, nombre: str | None, apellido: str | None, puesto: str | None, imagen: str | None):
        query = select(Empleado) # hace una lista inicial con todo por si no filtramos por ningún campo

        # Filtros dinámicos
        if id:
            query = query.where(Empleado.id == id)
        if nombre:
            # Consejo: .contains(nombre) permite buscar "Juan" escribiendo solo "Ju"
            #query = query.where(Empleado.nombre.contains(nombre))
            query = query.where(Empleado.nombre == nombre)
        if apellido:
            query = query.where(Empleado.apellido == apellido)
        if puesto:
            query = query.where(Empleado.puesto == puesto)
        if imagen:
            query = query.where(Empleado.imagen == imagen)

        return self.session.exec(query).all()

    # Te devuelve un empleado y si no lo encuentra, te manda un error
    def get_by_id(self, id: int):
        empleado = self.session.get(Empleado, id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return empleado

    def update(self, id: int, empleado_data: EmpleadoUpdate) -> Empleado:
        empleado = self.session.get(Empleado, id) #Primero lo busca
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado") #Si no lo encuentra sale un comentario

        empleado_dict = empleado_data.model_dump(exclude_unset=True) # Actualizara sin cambiar el resto de campos

        # busca en el objeto empleado la propiedad que se llame como la variable key y le asigna el value
        for key, value in empleado_dict.items():
            setattr(empleado, key, value)

        self.session.add(empleado)
        self.session.commit()
        self.session.refresh(empleado)
        return empleado

    def delete(self, id: int):
        empleado = self.session.get(Empleado, id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        self.session.delete(empleado)
        self.session.commit()
        return {"message": "Empleado eliminado correctamente"}

    async def save_image(self, file: UploadFile) -> str:
        upload_dir = "app/static/uploads"

        # Asegura que la carpeta existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Construye la ruta del archivo
        file_path = os.path.join(upload_dir, file.filename)

        # Guarda el contenido del archivo en el servidor
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Devuelve la ruta relativa para guardar en la BD
        return f"/static/uploads/{file.filename}"