import logging

from fastapi import APIRouter, HTTPException

from ...application.users.users_service import UsersService
from ...infra.users.mock_users_repository import MockUsersRepository
from ..dto.users_request import CreateUserRequest
from ..dto.users_response import CreateUserResponse, GetUserResponse

router = APIRouter()
log = logging.getLogger("app")

users_service = UsersService(repo=MockUsersRepository())


@router.post("/create")
async def create_user(request: CreateUserRequest) -> CreateUserResponse:
    res = users_service.create_user(username=request.username, age=request.age, email=request.email)
    if res:
        log.info(f"User created: {request.username}")
        return CreateUserResponse(result="ok")
    else:
        log.error("Failed to create user")
        return CreateUserResponse(result="Failed to create user")


@router.get("/{username}", response_model=GetUserResponse)
async def get_user(username: str) -> GetUserResponse:
    log.info("User lookup", extra={"username": username})

    user = users_service.get_user_by_username(username)
    if not user:
        log.warning("User not found", extra={"username": username})
        raise HTTPException(status_code=404, detail="User not found")

    log.info("User found", extra={"username": username})
    return GetUserResponse(username=user.username, age=user.age.value, email=user.email.value)
