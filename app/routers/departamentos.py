from fastapi import APIRouter, Depends
from app.schemas.departamento import DepartamentoCreate, DepartamentoResponse, DepartamentoUpdate
from app.services.departamento_service import DepartmentService

router = APIRouter(prefix="/departamentos", tags=["Departamentos"])


@router.post("/", response_model=DepartamentoResponse)
async def create_departamento(departamento: DepartamentoCreate, service: DepartmentService = Depends()):
    return service.create(departamento)

@router.get("/", response_model=list[DepartamentoResponse])
async def read_departamentos(service: DepartmentService = Depends()):
    return service.get_all()

@router.get("/{id}", response_model=DepartamentoResponse)
async def read_departamento(id: int, service: DepartamentoResponse = Depends()):
    return service.get_by_id(id)

@router.patch("/{id}", response_model=DepartamentoResponse)
async def update_departamento(id: int, departamento_data: DepartamentoUpdate, service: DepartmentService = Depends()):
    return service.update(id, departamento_data)

@router.delete("/{id}", response_model=dict)
async def delete_departamento(id: int, service: DepartmentService = Depends()):
    return service.delete(id)