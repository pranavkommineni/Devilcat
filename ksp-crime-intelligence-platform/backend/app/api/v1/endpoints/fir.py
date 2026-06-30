"""
fir.py
------
Minimal FIR CRUD endpoints. Demonstrates the full request path:
auth -> RBAC -> schema validation -> datastore_repo -> graph_repo edge writes.
Later phases (excel_importer, fir_sync) write through this same service
layer, not directly to the repo, so business rules stay centralized.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import CurrentUser, require_permission
from app.models.enums import GraphEdgeType, GraphNodeType
from app.models.fir import FIR
from app.models.graph import GraphEdge
from app.data_access.datastore_repo import DataStoreRepo
from app.data_access.graph_repo import graph_repo

router = APIRouter(prefix="/fir", tags=["FIR"])
fir_repo = DataStoreRepo(table_name="FIR", model_cls=FIR)


@router.post("", response_model=FIR, status_code=status.HTTP_201_CREATED)
async def create_fir(
    fir: FIR, current_user: CurrentUser = Depends(require_permission("fir:write"))
) -> FIR:
    created = await fir_repo.create(fir)

    # Write graph edges for every suspect/victim named on the incident so
    # link-analysis is queryable immediately, not as a deferred batch job.
    incident_id = created.incident.incident_id or created.fir_id
    for suspect_id in created.incident.suspect_ids:
        await graph_repo.add_edge(
            GraphEdge(
                source_id=suspect_id,
                source_type=GraphNodeType.SUSPECT,
                target_id=incident_id,
                target_type=GraphNodeType.INCIDENT,
                edge_type=GraphEdgeType.SUSPECT_OF,
                occurred_at=created.incident.occurred_at,
            )
        )
    for victim_id in created.incident.victim_ids:
        await graph_repo.add_edge(
            GraphEdge(
                source_id=victim_id,
                source_type=GraphNodeType.VICTIM,
                target_id=incident_id,
                target_type=GraphNodeType.INCIDENT,
                edge_type=GraphEdgeType.VICTIM_OF,
                occurred_at=created.incident.occurred_at,
            )
        )
    return created


@router.get("/{fir_id}", response_model=FIR)
async def get_fir(
    fir_id: str, current_user: CurrentUser = Depends(require_permission("fir:read"))
) -> FIR:
    fir = await fir_repo.get(fir_id)
    if fir is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found"
        )
    return fir


@router.get("", response_model=list[FIR])
async def list_firs(
    district: str | None = None,
    category: str | None = None,
    limit: int = 50,
    current_user: CurrentUser = Depends(require_permission("fir:read")),
) -> list[FIR]:
    clauses = []
    if district:
        clauses.append(f"District = '{district}'")
    if category:
        clauses.append(f"Incident.Category = '{category}'")
    where = " AND ".join(clauses) if clauses else "FirId IS NOT NULL"
    return await fir_repo.query(where, max_rows=min(limit, 200))
