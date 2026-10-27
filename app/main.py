from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    1: {
        "id": 1,
        "weight": 1.2,
        "content": "wooden table",
        "status": "in transit",
    },
    2: {
        "id": 2,
        "weight": 0.5,
        "content": "plastic chair",
        "status": "delivered",
    },
    3: {
        "id": 3,
        "weight": 2.0,
        "content": "metal shelf",
        "status": "pending",
    },
}

def log_request():

    def add_log(func):
        async def wrapper(*args, **kwargs):
            print("Route accessed")
            return await func(*args, **kwargs)
        return wrapper

    return add_log


@app.get("/shipment")
@log_request()
def get_shipment(id: int) -> dict[str, str | float | int]:
    if not id:
        return shipments[max(shipments.keys())]
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments[id]

@app.get("/shipment/latest")
@log_request()
def get_latest_shipment() -> dict[str, str | float | int]:
    return shipments[max(shipments.keys())]


@app.get("/shipment/{id}")
@log_request()
def get_shipment(id: int) -> dict[str, str | float | int]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments[id]


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )