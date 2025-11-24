import json
import logging
import os
import secrets

import redis
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.config import Config

router = APIRouter()
log = logging.getLogger("app")

GOOGLE_AUTH_REDIRECT_URL = os.getenv(
    "GOOGLEAUTH_REDIRECT_URL", "http://localhost:8080/auth/callback"
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)

config = Config(
    environ={
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID", ""),
        "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET", ""),
    }
)
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/admob.readonly"
    },
)


@router.get("/login")
async def google_login(request: Request) -> RedirectResponse:
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    nonce = secrets.token_urlsafe(32)
    request.session["oauth_nonce"] = nonce

    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_AUTH_REDIRECT_URL,
        state=state,
        nonce=nonce,
        access_type="offline",
        prompt="consent",
    )


@router.get("/callback", response_model=None)
async def google_callback(request: Request, response: Response) -> RedirectResponse | JSONResponse:
    received_state = request.query_params.get("state")
    stored_state = request.session.get("oauth_state")

    if not received_state or not stored_state or received_state != stored_state:
        log.warning(
            "OAuth state mismatch - possible CSRF attack",
            extra={"extra": {"service": "auth", "event": "csrf_detected"}},
        )
        return JSONResponse(content={"error": "Invalid state parameter"}, status_code=400)

    request.session.pop("oauth_state", None)

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        log.error(f"OAuth callback error: {e}")
        return JSONResponse(content={"error": "認可コードが見つかりません"}, status_code=400)

    id_token = token.get("id_token")
    stored_nonce = request.session.get("oauth_nonce")
    user_info = token.get("userinfo")

    if not (id_token and stored_nonce and user_info):
        log.error(
            "Missing ID token, nonce, or user info in OAuth callback",
            extra={"extra": {"service": "auth", "event": "missing_oauth_data"}},
        )
        return JSONResponse(content={"error": "不正なトークン情報"}, status_code=400)

    claims = token.get("id_token_claims") or user_info
    token_nonce = claims.get("nonce")

    if not token_nonce or token_nonce != stored_nonce:
        log.warning(
            "OAuth nonce mismatch - possible replay attack",
            extra={"extra": {"service": "auth", "event": "replay_attack_detected"}},
        )
        return JSONResponse(content={"error": "Invalid nonce parameter"}, status_code=400)

    request.session.pop("oauth_nonce", None)

    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = secrets.token_urlsafe(32)

    session_data = {
        "user": dict(user_info),
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "token_type": token.get("token_type", "Bearer"),
        "scope": token.get("scope", ""),
    }
    redis_client.setex(f"session:{session_id}", 3600, json.dumps(session_data))

    redirect = RedirectResponse(url="/auth/logged_in", status_code=303)
    redirect.set_cookie(
        key="session_id", value=session_id, httponly=True, secure=True, samesite="lax", max_age=3600
    )

    log.info(
        "User logged in successfully",
        extra={
            "extra": {
                "service": "auth",
                "event": "login_success",
                "scopes": token.get("scope", ""),
                "user_email": user_info.get("email") if user_info else None,
            }
        },
    )

    return redirect


@router.get("/logged_in")
async def check_logged_in(request: Request, response: Response) -> dict:
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"logged_in": False}

    session_data_str = redis_client.get(f"session:{session_id}")
    if not session_data_str:
        return {"logged_in": False}

    session_data = json.loads(str(session_data_str))
    user = session_data.get("user")
    access_token = session_data.get("access_token")

    if user and access_token:
        return {
            "logged_in": True,
            "user": user["email"],
        }
    else:
        return {"logged_in": False}


@router.get("/logout")
async def trigger_logout(request: Request, response: Response) -> dict:
    session_id = request.cookies.get("session_id")
    if session_id:
        redis_client.delete(f"session:{session_id}")

    response.delete_cookie("session_id")

    return {"result": "logout endpoint"}
