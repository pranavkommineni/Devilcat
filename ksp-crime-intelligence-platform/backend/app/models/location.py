from typing import Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    """
    Geo + administrative location, reused across FIR, Incident, and GIS layers.
    lat/lng stored at fixed precision to keep Data Store indexing stable and
    to make hotspot grid-bucketing (analytics_engine.spatiotemporal) deterministic.
    """

    location_id: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    district: str
    police_station: str
    address_text: Optional[str] = None
    pincode: Optional[str] = None

    # Precomputed S2/geohash-style cell for O(1) hotspot bucket lookups.
    # Populated by ingestion pipeline, not by the client.
    geo_cell: Optional[str] = None
