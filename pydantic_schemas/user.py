from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birthday: date
    role: int
    is_active: bool
    phone: Optional[str] = None


class UserCreate(UserBase):
    ...


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
