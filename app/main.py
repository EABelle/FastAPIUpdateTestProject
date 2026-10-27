from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference

from .db import shipments
from .modelschemas import Shipment, ShipmentStatus
from .apischemas import ShipmentCreateUpdateRequest, ShipmentCUDResponse, ShipmentPatchRequest

app = FastAPI()


def validate_shipment(shipment: ShipmentCreateUpdateRequest):
    if not shipment.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty")
    if not shipment.weight or shipment.weight <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weight must be positive")
    if shipment.weight > 25:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weight exceeds maximum limit of 25")

@app.get("/shipment/latest")
def get_latest_shipment() -> Shipment:
    return shipments[max(shipments.keys())]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> Shipment:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments[id]


@app.post("/shipment")
def create_shipment(shipment: ShipmentCreateUpdateRequest) -> ShipmentCUDResponse:

    validate_shipment(shipment)

    new_id = int(max(shipments.keys(), default=0)) + 1
    shipment = Shipment(
        id=new_id,
        weight=shipment.weight,
        content=shipment.content,
        status=ShipmentStatus.PENDING
    )
    shipments[new_id] = shipment
    return ShipmentCUDResponse(id=shipment.id)

@app.put("/shipment/{id}")
def update_shipment(id: int, shipment: ShipmentCreateUpdateRequest) -> ShipmentCUDResponse:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    validate_shipment(shipment)

    updated_shipment = Shipment(
        id=id,
        weight=shipment.weight,
        content=shipment.content,
        status=shipments[id].status
    )
    shipments[id] = updated_shipment
    return ShipmentCUDResponse(id=updated_shipment.id)

@app.patch("/shipment/{id}")
def patch_shipment(id: int, shipment: ShipmentPatchRequest) -> ShipmentCUDResponse:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    existing_shipment = shipments[id]
    updated_shipment = Shipment(
        id=id,
        weight=existing_shipment.weight,
        content=existing_shipment.content,
        status=shipment.status
    )
    shipments[id] = updated_shipment
    return ShipmentCUDResponse(id=updated_shipment.id)

@app.delete("/shipment/{id}")
def delete_shipment(id: int) -> ShipmentCUDResponse:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    shipments.pop(id)
    return ShipmentCUDResponse(id=id)

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )