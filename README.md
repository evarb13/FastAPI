# AP_FastAPI
API REST desarrollada con FastAPI para la gestión de servicios backend de forma rápida, eficiente y escalable.
## Descripción
Este proyecto está desarrollado con [FastAPI](https://fastapi.tiangolo.com/), un framework moderno para construir APIs con Python 3.10+ basado en tipado estándar.

Incluye:
- Alta performance
- Documentación automática (Swagger y ReDoc)
- Soporte para Docker
- Configuración mediante variables de entorno
- Uso de Postgres
## Tecnologías utilizadas
- Python 3.10+
- FastAPI
- Uvicorn
- Docker
## 1.  Clonar repositorio
git clone https://github.com/evarb13/AP_FastAPI.git
cd AP_FastAPI
## 2.  Variables de entorno
- Ejemplo
API_HOST=localhost:puerto
DB_HOST=db
DB_TYPE=postgresql
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_PORT=5432
POSTGRES_DB=nombre_db
## 3.  docker-compose
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: nombre_db
    ports:
      - "5432:5432"

  api:
    image: employee_api
    build: .
    depends_on:
      - db
    ports:
      - "puerto:puerto"
## 4.  Dockerfile
FROM python:3.14-alpine

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE puerto

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "puerto"]
## Paso 1
Ejecuta el docker-compose
## Paso 2
Escribe en tu navegador para poder usar la API:
http://localhost:puerto/docs
## EXTRA
Es necesario crear un departamento promero para poder crear un empleado
- Para ver los empleados: http://localhost:puerto/empleados
- Para ver los departamentos: http://localhost:puerto/departamentos
