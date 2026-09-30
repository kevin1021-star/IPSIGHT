"""
CIPHER-SENTINEL: Supabase client wrapper with seamless local fallback.

Exports
-------
supabase          – initialized Supabase client (service-role key) or None in local mode
get_supabase_client() – return client or None
upload_file()     – upload bytes to Supabase Storage bucket (or local disk fallback)
get_file()        – download bytes from bucket / disk
verify_jwt()      – verify JWT and return user payload dict
create_access_token() – generate local JWT when Supabase is not configured
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from jose import JWTError, jwt
from pydantic_settings import BaseSettings, SettingsConfigDict
from supabase import Client, create_client

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class _SupabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SECRET_KEY: str = "cipher-sentinel-jwt-secret-key-2026"
    ALGORITHM: str = "HS256"
    SUPABASE_BUCKET: str = "cipher-sentinel-uploads"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440


_cfg = _SupabaseSettings()

# ---------------------------------------------------------------------------
# Client (service-role key for backend API operations)
# ---------------------------------------------------------------------------

supabase: Optional[Client] = None

if _cfg.SUPABASE_URL and _cfg.SUPABASE_SERVICE_KEY:
    try:
        supabase = create_client(_cfg.SUPABASE_URL, _cfg.SUPABASE_SERVICE_KEY)
        logger.info("Connected to Supabase at %s", _cfg.SUPABASE_URL)
    except Exception as exc:
        logger.warning("Could not initialize Supabase client: %s. Falling back to local mode.", exc)
        supabase = None
else:
    logger.info("No SUPABASE_URL configured — operating in standalone local mode.")


def get_supabase_client() -> Optional[Client]:
    """Return the Supabase service client, or None if in local mode."""
    return supabase


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------

_LOCAL_UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
_LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def upload_file(bucket: str, path: str, content_bytes: bytes, content_type: str = "application/octet-stream") -> str:
    """
    Upload content_bytes to Supabase Storage if configured; otherwise save to local disk.
    """
    if supabase is not None:
        try:
            supabase.storage.from_(bucket).upload(
                path=path,
                file=content_bytes,
                file_options={"content-type": content_type, "upsert": "true"},
            )
            public_url = supabase.storage.from_(bucket).get_public_url(path)
            logger.info("Uploaded to Supabase Storage %s/%s → %s", bucket, path, public_url)
            return public_url
        except Exception as exc:
            logger.warning("Supabase storage upload error: %s. Saving locally.", exc)

    # Local storage fallback
    local_target = _LOCAL_UPLOAD_DIR / path.replace("/", os.sep)
    local_target.parent.mkdir(parents=True, exist_ok=True)
    local_target.write_bytes(content_bytes)
    logger.info("Saved file locally at %s", local_target)
    return str(local_target)


def get_file(bucket: str, path: str) -> bytes:
    """
    Download bytes from Supabase Storage or read from local disk.
    """
    if supabase is not None:
        try:
            return supabase.storage.from_(bucket).download(path)
        except Exception as exc:
            logger.warning("Supabase download error: %s. Checking local disk.", exc)

    local_target = _LOCAL_UPLOAD_DIR / path.replace("/", os.sep)
    if local_target.exists():
        return local_target.read_bytes()
    raise FileNotFoundError(f"File not found: {path}")


# ---------------------------------------------------------------------------
# JWT tokens & verification
# ---------------------------------------------------------------------------

def create_access_token(user_id: str, email: str, role: str = "authenticated") -> str:
    """Create a signed JWT token for the user."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=_cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(to_encode, _cfg.SECRET_KEY, algorithm=_cfg.ALGORITHM)


def verify_jwt(token: str) -> dict:
    """
    Verify a JWT using SECRET_KEY.
    """
    try:
        payload = jwt.decode(
            token,
            _cfg.SECRET_KEY,
            algorithms=[_cfg.ALGORITHM],
            options={"verify_aud": False},
        )
        return payload
    except JWTError as exc:
        logger.warning("JWT verification failed: %s", exc)
        raise
