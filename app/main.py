from fastapi import FastAPI
from app.routers import empleados, departamentos
from app.db.session import engine

from sqlmodel import SQLModel
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="API Directorio de Empleados")

upload_dir = os.path.join("app", "static", "uploads")
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(empleados.router)
app.include_router(departamentos.router)

def init_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    init_db()