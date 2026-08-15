from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=6, max_length=72)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
