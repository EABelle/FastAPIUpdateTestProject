from .modelschemas import Shipment, ShipmentStatus

shipments = {
    1: Shipment(
        id=1,
        weight=1.2,
        content="wooden table",
        status=ShipmentStatus.PENDING
    ),
    2: Shipment(
        id=2,
        weight=0.5,
        content="plastic chair",
        status=ShipmentStatus.DELIVERED
    ),
    3: Shipment(
        id=3,
        weight=2.0,
        content="metal shelf",
        status=ShipmentStatus.IN_TRANSIT
    ),
}