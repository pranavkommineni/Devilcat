"""
graph_repo.py
-------------
Implements link-analysis adjacency queries over the single GraphEdge table
described in docs/data-model.md. This is the only module that should know
the edge-table schema details — analytics_engine and API endpoints call
through this interface so the underlying storage (Catalyst Data Store today,
potentially a real graph DB later) can change without touching callers.
"""

from collections import defaultdict
from typing import Optional

from app.core.catalyst_client import catalyst
from app.models.enums import GraphEdgeType, GraphNodeType
from app.models.graph import GraphEdge

EDGE_TABLE = "GraphEdge"


class GraphRepo:
    def _table(self):
        return catalyst.datastore().table(EDGE_TABLE)

    async def add_edge(self, edge: GraphEdge) -> GraphEdge:
        payload = edge.model_dump(exclude_none=True, mode="json")
        row = await self._table().insert_row(payload)
        return GraphEdge.model_validate(row)

    async def forward_adjacency(
        self,
        source_id: str,
        edge_type: Optional[GraphEdgeType] = None,
        limit: int = 100,
    ) -> list[GraphEdge]:
        """Outgoing edges from a node — e.g. all incidents a suspect appears in."""
        clause = f"SourceId = '{source_id}'"
        if edge_type:
            clause += f" AND EdgeType = '{edge_type.value}'"
        return await self._query(clause, limit)

    async def reverse_adjacency(
        self,
        target_id: str,
        edge_type: Optional[GraphEdgeType] = None,
        limit: int = 100,
    ) -> list[GraphEdge]:
        """Incoming edges to a node — e.g. all suspects linked to an incident."""
        clause = f"TargetId = '{target_id}'"
        if edge_type:
            clause += f" AND EdgeType = '{edge_type.value}'"
        return await self._query(clause, limit)

    async def neighbors(
        self, node_id: str, hops: int = 1, limit_per_hop: int = 50
    ) -> dict[str, list[GraphEdge]]:
        """
        BFS-style multi-hop expansion for the network-graph viewer.
        Returns {node_id: [edges]} so the frontend can render a force-directed
        graph without N+1 round trips. Capped at `hops` to keep response time
        bounded for highly-connected hub suspects.
        """
        visited: set[str] = {node_id}
        frontier = [node_id]
        result: dict[str, list[GraphEdge]] = defaultdict(list)

        for _ in range(max(1, hops)):
            next_frontier: list[str] = []
            for nid in frontier:
                fwd = await self.forward_adjacency(nid, limit=limit_per_hop)
                rev = await self.reverse_adjacency(nid, limit=limit_per_hop)
                for e in fwd + rev:
                    result[nid].append(e)
                    other = e.target_id if e.source_id == nid else e.source_id
                    if other not in visited:
                        visited.add(other)
                        next_frontier.append(other)
            frontier = next_frontier
            if not frontier:
                break
        return dict(result)

    async def repeat_offender_links(
        self, suspect_id: str, limit: int = 100
    ) -> list[GraphEdge]:
        """All incidents a suspect is tied to, ordered implicitly by occurred_at desc via ZCQL."""
        clause = f"SourceId = '{suspect_id}' AND EdgeType = '{GraphEdgeType.SUSPECT_OF.value}'"
        return await self._query(clause, limit, order_by="OccurredAt DESC")

    async def _query(
        self, where_clause: str, limit: int, order_by: Optional[str] = None
    ) -> list[GraphEdge]:
        zcql = catalyst.app.zcql()
        order_sql = f" ORDER BY {order_by}" if order_by else ""
        query = (
            f"SELECT * FROM {EDGE_TABLE} WHERE {where_clause}{order_sql} LIMIT {limit}"
        )
        rows = await zcql.execute_query(query)
        return [GraphEdge.model_validate(r[EDGE_TABLE]) for r in rows]


graph_repo = GraphRepo()
