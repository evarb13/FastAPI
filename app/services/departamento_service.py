from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.departamento import Departamento
from app.schemas.departamento import DepartamentoCreate, DepartamentoResponse, DepartamentoUpdate


class DepartmentService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def create(self, departamento_data: DepartamentoCreate) -> DepartamentoResponse:
        departamento = Departamento(**departamento_data.model_dump())
        self.session.add(departamento)
        self.session.commit()
        self.session.refresh(departamento)
        return DepartamentoResponse(**departamento.model_dump())

    #consulta simple que devuelve una tabla entera
    def get_all(self):
        # recupera todos los registros de la tabla Departamento
        return self.session.exec(select(Departamento)).all()

    def get_by_id(self, id: int):
        return self.session.get(Departamento, id)

    def update(self, id: int, departamento_data: DepartamentoUpdate) -> Departamento:
        departamento = self.session.get(Departamento, id)
        if not departamento:
            raise HTTPException(status_code=404, detail="Departamento no encontrado")

        departamento_dict = departamento_data.model_dump(exclude_unset=True)
        for key, value in departamento_dict.items():
            setattr(departamento, key, value)

        self.session.add(departamento)
        self.session.commit()
        self.session.refresh(departamento)
        return departamento

    def delete(self, id: int):
        autor = self.session.get(Departamento, id)
        if not autor:
            raise HTTPException(status_code=404, detail="Departamento no encontrado")
        self.session.delete(autor)
        self.session.commit()
        return {"message": "Departamento eliminado exitosamente"}