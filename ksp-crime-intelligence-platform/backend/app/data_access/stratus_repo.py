"""
stratus_repo.py
----------------
Evidence file (image/video/PDF) storage over Catalyst Stratus.
Returns object keys only (never raw bytes through the API layer) — the
frontend fetches signed URLs separately to keep evidence transfer off the
FastAPI request/response cycle and avoid loading large files into app memory.
"""

from typing import Optional

from app.core.catalyst_client import catalyst

EVIDENCE_BUCKET = "crime-evidence"


class StratusRepo:
    def _bucket(self):
        return catalyst.stratus().bucket(EVIDENCE_BUCKET)

    async def upload(
        self, object_key: str, file_bytes: bytes, content_type: str
    ) -> str:
        await self._bucket().put_object(
            object_key, file_bytes, content_type=content_type
        )
        return object_key

    async def get_signed_url(self, object_key: str, expiry_minutes: int = 15) -> str:
        return await self._bucket().get_presigned_url(
            object_key, expiry_in_minutes=expiry_minutes
        )

    async def delete(self, object_key: str) -> bool:
        await self._bucket().delete_object(object_key)
        return True

    async def list_for_fir(self, fir_id: str) -> list[str]:
        objects = await self._bucket().list_objects(prefix=f"fir/{fir_id}/")
        return [o["object_key"] for o in objects]

    @staticmethod
    def evidence_key(fir_id: str, filename: str) -> str:
        return f"fir/{fir_id}/{filename}"


stratus_repo = StratusRepo()
