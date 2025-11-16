import logging
import os
import secrets

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.config import Config

router = APIRouter()
log = logging.getLogger("app")

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

    redirect_uri = "http://localhost:8080/auth/callback"
    return await oauth.google.authorize_redirect(
        request, redirect_uri, state=state, nonce=nonce, access_type="offline", prompt="consent"
    )


@router.get("/callback", response_model=None)
async def google_callback(request: Request) -> RedirectResponse | JSONResponse:
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

    request.session["user"] = dict(user_info)
    request.session["access_token"] = token.get("access_token")
    request.session["refresh_token"] = token.get("refresh_token")
    request.session["token_type"] = token.get("token_type", "Bearer")
    request.session["scope"] = token.get("scope", "")

    redirect = RedirectResponse(url="/auth/logged_in", status_code=303)
    redirect.set_cookie(
        key="scope", value=token.get("scope", ""), httponly=True, secure=True, samesite="lax"
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
    user = request.session.get("user")
    access_token = request.session.get("access_token")

    if user and access_token:
        response.set_cookie(
            key="access_token", value=access_token, httponly=True, secure=True, samesite="lax"
        )

        return {
            "logged_in": True,
            "user": user["email"],
        }
    else:
        return {"logged_in": False}


@router.get("/logout")
async def trigger_logout(request: Request) -> dict:
    request.session.clear()
    return {"result": "logout endpoint"}
