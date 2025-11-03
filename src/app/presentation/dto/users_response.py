from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    result: str


class GetUserResponse(BaseModel):
    username: str | None
    age: int | None
    email: str | None
