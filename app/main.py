from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

class ShipmentRequest(BaseModel):
    weight: float | int
    content: str

class Shipment(ShipmentRequest):
    id: int
    status: str

class ShipmentResponse(BaseModel):
    id: int

shipments = {
    1: Shipment(
        id=1,
        weight=1.2,
        content="wooden table",
        status="in transit",
    ),
    2: Shipment(
        id=2,
        weight=0.5,
        content="plastic chair",
        status="delivered",
    ),
    3: Shipment(
        id=3,
        weight=2.0,
        content="metal shelf",
        status="pending",
    ),
}

@app.get("/shipment/latest")
def get_latest_shipment() -> Shipment:
    return shipments[max(shipments.keys())]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> Shipment:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments[id]


@app.post("/shipment")
def create_shipment(shipment: ShipmentRequest) -> ShipmentResponse:

    if not shipment.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty")
    if not shipment.weight or shipment.weight <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weight must be positive")
    if shipment.weight > 25:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weight exceeds maximum limit of 25")

    new_id = max(shipments.keys()) + 1
    shipment = Shipment(
        id=new_id,
        weight=shipment.weight,
        content=shipment.content,
        status="pending"
    )
    shipments[new_id] = shipment
    return ShipmentResponse(id=shipment.id)


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )