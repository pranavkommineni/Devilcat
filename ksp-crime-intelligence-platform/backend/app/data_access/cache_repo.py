"""
cache_repo.py
-------------
Thin wrapper over Catalyst Cache for dashboard/query-result caching.
Keys are namespaced by segment to allow targeted invalidation
(e.g. invalidate only one district's hotspot cache on new FIR write)
instead of flushing the whole cache.
"""

import json
from typing import Any, Optional

from app.core.catalyst_client import catalyst
from app.core.config import get_settings

settings = get_settings()


class CacheRepo:
    def __init__(self, segment_name: str = "crimelens-default") -> None:
        self.segment_name = segment_name

    def _segment(self):
        return catalyst.cache().segment(self.segment_name)

    async def get_json(self, key: str) -> Optional[Any]:
        raw = await self._segment().get_value(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (TypeError, ValueError):
            return None

    async def set_json(
        self, key: str, value: Any, ttl_seconds: Optional[int] = None
    ) -> None:
        ttl = ttl_seconds or settings.cache_default_ttl_seconds
        await self._segment().put_value(
            key, json.dumps(value, default=str), expiry_in_minutes=max(1, ttl // 60)
        )

    async def invalidate(self, key: str) -> None:
        await self._segment().delete_value(key)

    @staticmethod
    def dashboard_key(district: str, date_range: str, category: str = "all") -> str:
        return f"dash:{district}:{date_range}:{category}"

    @staticmethod
    def adjacency_key(node_id: str, hops: int) -> str:
        return f"adj:{node_id}:{hops}"


cache_repo = CacheRepo()
