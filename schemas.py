from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    full_name: str
    email: str
    password: str

class CreateEntryRequest(BaseModel):
    post: str
    mood: int
    user_username: str
    date: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None