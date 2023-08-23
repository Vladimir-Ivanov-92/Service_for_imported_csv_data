import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

# numbers, lowercase letters, symbols - and _
# length is from 3 to 16 characters:
LOGIN_MATCH_PATTERN = re.compile(r"^[a-z0-9_-]{3,16}$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowUser(TunedModel):
    """fields returned to the client"""
    user_id: uuid.UUID
    login: str
    email: str
    is_active: bool


class UserCreate(BaseModel):
    """incoming request processing model"""
    login: str
    email: EmailStr

    @field_validator("login")
    def validate_login(cls, value):
        if not LOGIN_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Укажите логин используя: цифры, строчные буквы, \
                       символы - и _ (длина – от 3 до 16 знаков)."
            )
        return value
