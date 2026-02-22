from fastapi import APIRouter, Depends, Query, UploadFile, File
from app.services.empleado_service import EmpleadoService
from app.schemas.empleado import EmpleadoCreate, EmpleadoResponse, EmpleadoUpdate

router = APIRouter(prefix="/empleados", tags=["Empleado"])

@router.post("/", response_model=EmpleadoResponse)
async def create_empleado(empleado: EmpleadoCreate, service: EmpleadoService = Depends()):
    return service.create(empleado)

@router.get("/", response_model=list[EmpleadoResponse])
async def read_empleados(service: EmpleadoService = Depends(),
                         id: int | None = Query(None, description="Filtrar por ID del empleado"),
                         nombre: str | None = Query(None, description="Filtrar por nombre"),
                         apellido: str | None = Query(None, description="Filtrar por apellido"),
                         puesto: str | None = Query(None, description="Filtrar por puesto"),
                         imagen_uri: str | None = Query(None, description="Filtrar por imagen")):
    # En caso de que haya algun filtro se veria de esta forma URL sería:
    # http://localhost:8000/empleados/?nombre=Ana&puesto=Programadora
    return service.get_all(id, nombre, apellido, puesto, imagen_uri)

@router.get("/{id}", response_model=EmpleadoResponse)
async def read_empleado(id: int, service: EmpleadoService = Depends()):
    return service.get_by_id(id)

@router.patch("/{id}", response_model=EmpleadoResponse)
async def update_empleado(id: int, empleado_data: EmpleadoUpdate, service: EmpleadoService = Depends()):
    return service.update(id, empleado_data)

@router.delete("/{id}", response_model=dict)
async def delete_empleado(id: int, service: EmpleadoService = Depends()):
    return service.delete(id)

@router.patch("/{id}/image", response_model=EmpleadoResponse)
async def upload_empleado_image(
        id: int,
        file: UploadFile = File(...),
        service: EmpleadoService = Depends()
):
    # 1. Guardamos la imagen físicamente y obtenemos la ruta
    image_url = await service.save_image(file)

    # 2. Creamos un objeto de actualización con esa ruta
    empleado_update = EmpleadoUpdate(imagen=image_url)

    # 3. Reutilizamos tu metodo update para guardar la ruta en la BD
    return service.update(id, empleado_update)