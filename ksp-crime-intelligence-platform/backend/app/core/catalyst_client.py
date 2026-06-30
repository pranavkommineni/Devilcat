"""
catalyst_client.py
------------------
Single point of initialization for the Zoho Catalyst Python SDK.
Every repository (datastore_repo, graph_repo, cache_repo, stratus_repo) pulls
its handle from here instead of re-initializing the SDK, which would be slow
and would create duplicate connection pools under load.

Usage:
    from app.core.catalyst_client import catalyst

    table = catalyst.datastore().table("FIR")
    cache_segment = catalyst.cache().segment("dashboard")
"""

from functools import lru_cache
from typing import Optional

import zcatalyst_sdk

from app.core.config import get_settings

settings = get_settings()


class CatalystClient:
    """
    Thin lazy-init wrapper around the Catalyst App so we only pay the
    initialization cost once per process (per AppSail worker), not per-request.
    """

    def __init__(self) -> None:
        self._app: Optional["zcatalyst_sdk.CatalystApp"] = None

    def _init_app(self) -> "zcatalyst_sdk.CatalystApp":
        # In AppSail, the SDK auto-detects project credentials from the
        # deployment environment. Locally, it reads catalyst_credential_json_path.
        app = zcatalyst_sdk.initialize(
            project_id=settings.catalyst_project_id,
            environment=settings.catalyst_environment,
        )
        return app

    @property
    def app(self):
        if self._app is None:
            self._app = self._init_app()
        return self._app

    def datastore(self):
        return self.app.datastore()

    def cache(self):
        return self.app.cache()

    def stratus(self):
        return self.app.stratus()

    def authentication(self):
        return self.app.authentication()

    def search(self):
        return self.app.search()

    def function(self):
        return self.app.function()


@lru_cache
def _get_client() -> CatalystClient:
    return CatalystClient()


catalyst = _get_client()
