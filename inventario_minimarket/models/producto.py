from dataclasses import dataclass, asdict


@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float
    stock: int
    stock_minimo: int
    vencimiento: str = ""

    def to_dict(self):
        return asdict(self)
