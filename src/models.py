from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    """Representa um ponto geográfico validado."""
    address: str
    latitude: float
    longitude: float
    is_start_point: bool = False

class RoutePlan(BaseModel):
    """Representa o plano final de entrega."""
    raw_input: str
    stops: List[Location]
    total_distance_km: float