from datetime import datetime
from typing import Optional, List, Annotated

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator

class UserCreate(BaseModel):
    nombre: str
    email: str
    foto_perfil: Optional[str]
    telefono: Optional[str]

class EmpresaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str]
    ubicacion: Optional[str]

class EmpleoCreate(BaseModel):
    titulo: str
    descripcion: Optional[str]
    categoria: Optional[str]
    ubicacion: Optional[str]
    habilidades: List[str]


PyObjectId = Annotated[str, BeforeValidator(str)]


class Job(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    skills: List[str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

