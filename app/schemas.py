from typing import Optional, List, Annotated

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator


class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


PyObjectId = Annotated[str, BeforeValidator(str)]


class Example(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    test: str
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class ExampleCollection(BaseModel):
    examples: List[Example]