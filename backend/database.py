# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session

# Carga .env ANTES de leer variables
load_dotenv()

# Usa por defecto tu usuario/BD (por si .env no se encuentra)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://alumnodb:alumnodb@localhost:5432/juegosdb"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()