from enum import Enum

from pydantic import BaseModel, Field

class ShipmentStatus(str, Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class ShipmentBaseModel(BaseModel):
    destination: int | None = Field(default=None)
    weight: float = Field(lt=25, gt=0)
    content: str = Field(max_length=100)

class Shipment(ShipmentBaseModel):
    id: int
    destination: int | None = Field(default=None)
    status: ShipmentStatus
