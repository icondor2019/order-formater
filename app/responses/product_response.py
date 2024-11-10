from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    uuid: str = Field(...)
    seller_uuid: str = Field(...)
    product_uuid: str = Field(...)
    raw_description: str = Field(default=None)
    stock: int = Field(...)
    price: float = Field(...)
    status: str = Field(default='active')

    class Config:
        from_attributes = True
