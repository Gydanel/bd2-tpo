from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from models import Base

DB_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def start_up():
    Base.metadata.create_all(bind=engine)
    print("✅ creadas las tablas")