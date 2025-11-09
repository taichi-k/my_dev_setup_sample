import logging

from fastapi import APIRouter, Depends, HTTPException

from app.application.users.users_service import UsersService
from app.domain.common.email import Email
from app.presentation.controllers.users_deps import get_users_service
from app.presentation.dto.users_request import CreateUserRequest
from app.presentation.dto.users_response import CreateUserResponse, GetUserResponse

router = APIRouter()
log = logging.getLogger("app")


@router.post("/create")
async def create_user(
    request: CreateUserRequest,
    users_service: UsersService = Depends(get_users_service),
) -> CreateUserResponse:
    res = await users_service.create_user(
        username=request.username, age=request.age, email=Email(request.email)
    )
    if res:
        log.info(f"User created: {request.username}")
        return CreateUserResponse(result="ok")
    else:
        log.error("Failed to create user")
        return CreateUserResponse(result="Failed to create user")


@router.get("/{username}", response_model=GetUserResponse)
async def get_user(
    username: str,
    users_service: UsersService = Depends(get_users_service),
) -> GetUserResponse:
    log.info("User lookup", extra={"username": username})

    user = await users_service.get_user_by_username(username)
    if not user:
        log.warning("User not found", extra={"username": username})
        raise HTTPException(status_code=404, detail="User not found")

    log.info("User found", extra={"username": username})
    return GetUserResponse(username=user.username, age=user.age.value, email=user.email.value)
