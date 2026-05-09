from dataclasses import dataclass, asdict


@dataclass
class Venta:
    fecha: str
    codigo: str
    producto: str
    cantidad: int
    precio_unitario: float
    total: float

    def to_dict(self):
        return asdict(self)
