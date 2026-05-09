from storage.json_storage import PRODUCTOS_FILE, cargar_json, guardar_json


class ProductoService:
    def __init__(self):
        self.productos = cargar_json(PRODUCTOS_FILE)

    def guardar(self):
        guardar_json(PRODUCTOS_FILE, self.productos)

    def listar(self):
        return self.productos

    def buscar_por_codigo(self, codigo):
        return next((p for p in self.productos if p["codigo"] == codigo), None)

    def buscar(self, texto):
        texto = texto.lower().strip()
        return [
            p for p in self.productos
            if texto in p["codigo"].lower()
            or texto in p["nombre"].lower()
            or texto in p["categoria"].lower()
        ]

    def registrar(self, producto):
        if self.buscar_por_codigo(producto["codigo"]):
            raise ValueError("Ya existe un producto con ese código.")
        self.productos.append(producto)
        self.guardar()

    def editar(self, codigo, nuevos_datos):
        producto = self.buscar_por_codigo(codigo)
        if not producto:
            raise ValueError("Producto no encontrado.")
        producto.update(nuevos_datos)
        self.guardar()

    def eliminar(self, codigo):
        producto = self.buscar_por_codigo(codigo)
        if not producto:
            raise ValueError("Producto no encontrado.")
        self.productos.remove(producto)
        self.guardar()

    def actualizar_stock(self, codigo, nuevo_stock):
        producto = self.buscar_por_codigo(codigo)
        if not producto:
            raise ValueError("Producto no encontrado.")
        producto["stock"] = nuevo_stock
        self.guardar()
