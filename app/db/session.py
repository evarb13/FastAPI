from sqlmodel import create_engine, Session
from app.core.config import config
from sqlalchemy import URL

connect_args = {}
if config.db_type.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    database_url = "sqlite:///./database.db"
else:
    database_url = URL.create(
        drivername=config.db_type,
        username=config.postgres_user,
        password=config.postgres_password,
        host=config.db_host,
        port=int(config.postgres_port),
        database=config.postgres_db,
    )

engine = create_engine(
    database_url,
    echo=config.debug,
    connect_args=connect_args
)

def get_session():
    with Session(engine) as session:
        yield session