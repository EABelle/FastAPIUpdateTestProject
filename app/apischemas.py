from pydantic import BaseModel, Field
from .modelschemas import Shipment, ShipmentBaseModel, ShipmentStatus


class ShipmentCreateUpdateRequest(ShipmentBaseModel):
    destination: int | None = Field(default=None)

class ShipmentPatchRequest(BaseModel):
    status: ShipmentStatus

class ShipmentResponse(Shipment):
    pass

class ShipmentCUDResponse(BaseModel):
    id: int
