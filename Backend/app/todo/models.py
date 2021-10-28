from typing import Optional
import uuid
from pydantic import BaseModel, Field


class CategoriesModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    # completed: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Motors",
                "description": "Motor sports and more",
            }
        }


class UpdateCategoriesModel(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Learn FARM Stack",
                "completed": "Motor sports and more",
            }
        }