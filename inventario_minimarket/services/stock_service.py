from datetime import datetime
from storage.json_storage import MOVIMIENTOS_FILE, cargar_json, guardar_json
from models.movimiento_stock import MovimientoStock


class StockService:
    def __init__(self, producto_service):
        self.producto_service = producto_service
        self.movimientos = cargar_json(MOVIMIENTOS_FILE)

    def guardar(self):
        guardar_json(MOVIMIENTOS_FILE, self.movimientos)

    def listar_movimientos(self):
        return self.movimientos

    def mover_stock(self, codigo, cantidad, tipo, motivo):
        producto = self.producto_service.buscar_por_codigo(codigo)
        if not producto:
            raise ValueError("Producto no encontrado.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        if tipo == "INGRESO":
            producto["stock"] += cantidad
        elif tipo == "SALIDA":
            if cantidad > producto["stock"]:
                raise ValueError("No hay stock suficiente.")
            producto["stock"] -= cantidad
        else:
            raise ValueError("Tipo de movimiento no válido.")

        self.producto_service.guardar()

        movimiento = MovimientoStock(
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            codigo=codigo,
            producto=producto["nombre"],
            tipo=tipo,
            cantidad=cantidad,
            stock_resultante=producto["stock"],
            motivo=motivo
        ).to_dict()
        self.movimientos.append(movimiento)
        self.guardar()
        return producto
