from dataclasses import dataclass, asdict


@dataclass
class MovimientoStock:
    fecha: str
    codigo: str
    producto: str
    tipo: str
    cantidad: int
    stock_resultante: int
    motivo: str

    def to_dict(self):
        return asdict(self)
