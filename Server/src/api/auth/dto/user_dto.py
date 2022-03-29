from pydantic import BaseModel, Field, EmailStr, validator
import bcrypt


class UserDto(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    @validator("password")
    def create_hashed_password(cls, v):
        return bcrypt.hashpw(v.encode("utf8"), bcrypt.gensalt())
