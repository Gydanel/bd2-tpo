from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
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
    init_script()
    print("✅ creadas las tablas")

def init_script():
    with engine.connect() as con:
        with open("init.sql") as file:
            sql_script = file.read()
            for stmt in sql_script.split(";"):
                stmt = stmt.strip()
                if stmt:
                    con.execute(text(stmt))
            con.commit()