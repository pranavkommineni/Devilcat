"""
datastore_repo.py
------------------
Generic + typed CRUD repository over Catalyst Data Store tables.
All other repos/services should go through here rather than calling the
Catalyst SDK table API directly, so query patterns, retries, and error
handling stay consistent in one place.
"""

from typing import Any, Optional, TypeVar

from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.catalyst_client import catalyst

T = TypeVar("T", bound=BaseModel)


class DataStoreRepo:
    def __init__(self, table_name: str, model_cls: type[T]) -> None:
        self.table_name = table_name
        self.model_cls = model_cls

    def _table(self):
        return catalyst.datastore().table(self.table_name)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=2))
    async def get(self, row_id: str) -> Optional[T]:
        row = await self._table().get_row(row_id)
        if row is None:
            return None
        return self.model_cls.model_validate(row)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=2))
    async def create(self, item: T) -> T:
        payload = item.model_dump(exclude_none=True, mode="json")
        created_row = await self._table().insert_row(payload)
        return self.model_cls.model_validate(created_row)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=2))
    async def update(self, row_id: str, item: T) -> T:
        payload = item.model_dump(exclude_none=True, mode="json")
        payload["ROWID"] = row_id
        updated_row = await self._table().update_row(payload)
        return self.model_cls.model_validate(updated_row)

    async def delete(self, row_id: str) -> bool:
        await self._table().delete_row(row_id)
        return True

    async def query(self, zcql_where_clause: str, max_rows: int = 200) -> list[T]:
        """
        zcql_where_clause example: "Category = 'robbery' AND District = 'Bengaluru Urban'"
        Pagination via max_rows keeps dashboard queries bounded; callers needing
        more should paginate explicitly rather than requesting unbounded scans.
        """
        zcql = catalyst.app.zcql()
        query = f"SELECT * FROM {self.table_name} WHERE {zcql_where_clause} LIMIT {max_rows}"
        rows: list[dict[str, Any]] = await zcql.execute_query(query)
        return [self.model_cls.model_validate(r[self.table_name]) for r in rows]
