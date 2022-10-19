from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class UserSchema(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    email: str
    hashed_password: str
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    class Config:
        orm_model = True


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class LoginUser(BaseModel):  # Todo можно CreateUser сделать общий для создания и логина
    email: str
    password: str


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str