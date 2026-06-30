"""
login.py
--------
Authenticates a user against Catalyst Authentication, then issues our own
short-lived JWT carrying the resolved RBAC role so every other endpoint can
authorize with a fast, local token decode instead of a network round-trip.
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from app.auth.roles import Role
from app.core.catalyst_client import catalyst
from app.core.security import create_access_token
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """
    Validates credentials via Catalyst Authentication, then maps the
    authenticated user's Catalyst role/org-role to one of our 3 RBAC roles
    and mints a JWT. Role mapping logic lives in `_resolve_role`.
    """
    try:
        auth_service = catalyst.authentication()
        # NOTE: zcatalyst_sdk exposes server-side credential verification via
        # the Authentication component; exact method name depends on SDK
        # version — verify_user_credentials is the documented v2 call.
        user = auth_service.verify_user_credentials(
            email_id=form_data.username, password=form_data.password
        )
    except Exception as exc:  # noqa: BLE001 - SDK raises its own exception types
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        ) from exc

    role = _resolve_role(user)
    token = create_access_token(subject=str(user["user_id"]), role=role.value)
    return TokenResponse(access_token=token, token_type="bearer", role=role.value)


def _resolve_role(catalyst_user: dict) -> Role:
    """
    Maps the org_role/custom attribute set on the Catalyst user record to our
    internal Role enum. Adjust the attribute key to match how roles are
    provisioned in the Admin Portal (Phase 8).
    """
    raw_role = (catalyst_user.get("role_name") or "investigator").lower()
    try:
        return Role(raw_role)
    except ValueError:
        return Role.INVESTIGATOR
