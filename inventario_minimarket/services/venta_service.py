from datetime import datetime
from storage.json_storage import VENTAS_FILE, cargar_json, guardar_json
from models.venta import Venta


class VentaService:
    def __init__(self, producto_service, stock_service):
        self.producto_service = producto_service
        self.stock_service = stock_service
        self.ventas = cargar_json(VENTAS_FILE)

    def guardar(self):
        guardar_json(VENTAS_FILE, self.ventas)

    def listar(self):
        return self.ventas

    def registrar_venta(self, codigo, cantidad):
        producto = self.producto_service.buscar_por_codigo(codigo)
        if not producto:
            raise ValueError("Producto no encontrado.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        if cantidad > producto["stock"]:
            raise ValueError("No se puede vender más stock del disponible.")

        total = round(producto["precio"] * cantidad, 2)
        venta = Venta(
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            codigo=codigo,
            producto=producto["nombre"],
            cantidad=cantidad,
            precio_unitario=producto["precio"],
            total=total
        ).to_dict()

        self.stock_service.mover_stock(codigo, cantidad, "SALIDA", "Venta registrada")
        self.ventas.append(venta)
        self.guardar()
        return venta
