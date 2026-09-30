"""
CIPHER-SENTINEL: Auth router (Supabase-backed with local standalone fallback).

Routes
------
POST /api/auth/login    – sign in with email + password
POST /api/auth/register – sign up a new user
GET  /api/auth/me       – return current user info (requires Bearer token)
"""

from __future__ import annotations

import hashlib
import logging
import uuid
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from backend.supabase_client import (
    create_access_token,
    get_supabase_client,
    verify_jwt,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ---------------------------------------------------------------------------
# Pydantic request schemas
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str


# ---------------------------------------------------------------------------
# Dependency: resolve current user from Bearer token
# ---------------------------------------------------------------------------

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Verify JWT and return user payload."""
    try:
        payload = verify_jwt(token)
        return payload
    except Exception as exc:
        logger.warning("JWT verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/login")
async def login(body: LoginRequest) -> Dict[str, Any]:
    """Authenticate user via Supabase or local fallback."""
    supabase = get_supabase_client()
    if supabase is not None:
        try:
            resp = supabase.auth.sign_in_with_password(
                {"email": body.email, "password": body.password}
            )
            session = resp.session
            user = resp.user
            if not session or not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )
            return {
                "access_token": session.access_token,
                "token_type": "bearer",
                "expires_in": session.expires_in,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "created_at": str(user.created_at),
                },
            }
        except HTTPException:
            raise
        except Exception as exc:
            logger.warning("Supabase login failed (%s), trying local auth", exc)

    # Local / dev mode authentication: generate deterministic UUID based on email
    user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, body.email.strip().lower()))
    token = create_access_token(user_id=user_id, email=body.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 86400,
        "user": {
            "id": user_id,
            "email": body.email,
            "created_at": "2026-01-01T00:00:00Z",
        },
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest) -> Dict[str, Any]:
    """Register a new user via Supabase or local fallback."""
    supabase = get_supabase_client()
    if supabase is not None:
        try:
            resp = supabase.auth.sign_up({"email": body.email, "password": body.password})
            user = resp.user
            if user:
                return {
                    "message": "Registration successful.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "created_at": str(user.created_at),
                    },
                }
        except Exception as exc:
            logger.warning("Supabase register exception: %s", exc)

    # Local fallback
    user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, body.email.strip().lower()))
    token = create_access_token(user_id=user_id, email=body.email)
    return {
        "message": "Registration successful.",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": body.email,
            "created_at": "2026-01-01T00:00:00Z",
        },
    }


@router.get("/me")
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Return the current authenticated user's profile."""
    return {
        "id": current_user.get("sub"),
        "email": current_user.get("email"),
        "role": current_user.get("role", "authenticated"),
    }
