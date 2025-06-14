from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

# Tabla de usuarios
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now)

class Company(Base):
    __tablename__ = "Empresa"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Job(Base):
    __tablename__ = "Empleo"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("Empresa.id"))

