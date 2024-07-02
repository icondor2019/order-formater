from data_models.sellerEnum import SellerStatusEnum
from pydantic import BaseModel, Field
from datetime import datetime


class SellerResponse(BaseModel):
    uuid: str = Field(...)
    user_id: int = Field(...)
    name: str = Field(default='no_name')
    created_at: datetime = datetime.now()
    status: SellerStatusEnum = Field(default='pending')
