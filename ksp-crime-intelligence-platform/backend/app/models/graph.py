from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import GraphEdgeType, GraphNodeType


class GraphNode(BaseModel):
    """
    Generic node wrapper so suspects/victims/locations/incidents/phones/vehicles
    can all be referenced uniformly by graph_repo without needing a real graph DB.
    """

    node_id: str
    node_type: GraphNodeType
    label: str
    metadata: dict = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """
    THE central modeling decision of this platform (see docs/data-model.md):
    Catalyst Data Store is relational, not a native graph DB, so all
    relationship/link-analysis features are built on a single denormalized
    edge table instead of joins across many typed tables.

    Row shape mirrors this model 1:1. Every relationship in the system
    (suspect->incident, incident->location, suspect->suspect association,
    CDR contact graph, repeat-MO links) is one row here.

    Indexing strategy (see docs/data-model.md):
      - composite index on (source_id, edge_type)
      - composite index on (target_id, edge_type)
      - index on edge_type alone for full-graph queries (e.g. MO clustering)
    This keeps both forward and reverse adjacency lookups O(log n).
    """

    edge_id: Optional[str] = None
    source_id: str
    source_type: GraphNodeType
    target_id: str
    target_type: GraphNodeType
    edge_type: GraphEdgeType
    weight: float = Field(
        default=1.0, description="Association strength, e.g. # of shared incidents"
    )
    occurred_at: Optional[datetime] = None
    properties: dict = Field(
        default_factory=dict, description="Edge-specific extra attributes"
    )
    created_at: Optional[datetime] = None
