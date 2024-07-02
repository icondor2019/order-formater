from enum import Enum


class SellerStatusEnum(Enum):
    active: str = 'active'
    inactive: str = 'inactive'
    pending: str = 'pending'
