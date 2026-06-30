"""
roles.py
--------
Single source of truth for RBAC. Adding a new role or endpoint permission
should only ever require editing this file.
"""

from enum import Enum


class Role(str, Enum):
    INVESTIGATOR = "investigator"
    ANALYST = "analyst"
    ADMIN = "admin"


# Coarse-grained, per-resource-group permission table.
# Extend with finer scopes (e.g. "fir:write") if needed later.
ROLE_PERMISSIONS: dict[Role, set[str]] = {
    Role.INVESTIGATOR: {
        "fir:read",
        "fir:write",
        "victims:read",
        "victims:write",
        "crime:read",
        "network:read",
        "predictive:read",
        "conversational:use",
    },
    Role.ANALYST: {
        "fir:read",
        "victims:read",
        "crime:read",
        "cdr:read",
        "finance:read",
        "gis:read",
        "network:read",
        "predictive:read",
        "analytics:read",
        "conversational:use",
    },
    Role.ADMIN: {
        "fir:read",
        "fir:write",
        "victims:read",
        "victims:write",
        "crime:read",
        "crime:write",
        "cdr:read",
        "finance:read",
        "gis:read",
        "network:read",
        "predictive:read",
        "analytics:read",
        "conversational:use",
        "admin:users",
        "admin:roles",
        "admin:audit",
    },
}


def role_has_permission(role: Role, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())
