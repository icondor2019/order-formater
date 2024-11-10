from pydantic import BaseModel, Field
from typing import Optional


class CatalogueResponse(BaseModel):
    uuid: str = Field(...)
    name: Optional[str] = Field(None)
    size: int = Field(...)
    color: Optional[str] = Field(None)
    stems: int = Field(...)
    package: str = Field(default='HB')
    description: Optional[str] = Field(None)
    embedding: str = Field(...)

    class Config:
        from_attributes = True
