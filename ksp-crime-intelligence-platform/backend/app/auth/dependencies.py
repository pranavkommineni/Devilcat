"""
dependencies.py
----------------
FastAPI dependency-injection helpers for authentication and RBAC.
Endpoints declare requirements like:

    @router.get("/fir", dependencies=[Depends(require_permission("fir:read"))])
"""

from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.roles import Role, role_has_permission
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


@dataclass(frozen=True)
class CurrentUser:
    user_id: str
    role: Role


def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    role_value = payload.get("role")
    if user_id is None or role_value not in Role._value2member_map_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token claims"
        )
    return CurrentUser(user_id=user_id, role=Role(role_value))


def require_permission(permission: str):
    """Returns a FastAPI dependency that enforces a single permission string."""

    def _checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not role_has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role.value}' lacks permission '{permission}'",
            )
        return current_user

    return _checker


def require_role(*allowed_roles: Role):
    """Use when a whole endpoint is restricted to specific roles (e.g. admin-only)."""

    def _checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role.value}' is not permitted to access this resource",
            )
        return current_user

    return _checker
