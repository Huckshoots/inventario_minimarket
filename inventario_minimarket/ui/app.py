from datetime import datetime, date
import tkinter as tk
from tkinter import ttk, messagebox

from models.producto import Producto
from services.producto_service import ProductoService
from services.stock_service import StockService
from services.venta_service import VentaService
from services.reporte_service import ReporteService


class InventarioApp:
    """Interfaz gráfica PRO para MiniMarket Express usando Tkinter + JSON."""

    COLOR_PRIMARY = "#0F3D5E"
    COLOR_SECONDARY = "#145A7A"
    COLOR_ACCENT = "#2E86C1"
    COLOR_BG = "#F4F7FA"
    COLOR_CARD = "#FFFFFF"
    COLOR_DANGER = "#C0392B"
    COLOR_WARNING = "#F39C12"
    COLOR_SUCCESS = "#1E8449"
    COLOR_TEXT = "#1F2933"
    FORMATO_FECHA = "%d/%m/%Y"

    def __init__(self, root):
        self.root = root
        self.root.title("MiniMarket Express - Inventario PRO")
        self.root.geometry("1250x760")
        self.root.minsize(1150, 690)
        self.root.configure(bg=self.COLOR_BG)

        self.producto_service = ProductoService()
        self.stock_service = StockService(self.producto_service)
        self.venta_service = VentaService(self.producto_service, self.stock_service)
        self.reporte_service = ReporteService(self.producto_service, self.venta_service)

        self.configurar_estilos()
        self.crear_interfaz()
        self.refrescar_todo()

    # ------------------------------------------------------------------
    # ESTILOS GENERALES
    # ------------------------------------------------------------------
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=self.COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=[18, 10], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.COLOR_CARD)], foreground=[("selected", self.COLOR_PRIMARY)])

        style.configure("TFrame", background=self.COLOR_BG)
        style.configure("Card.TFrame", background=self.COLOR_CARD, relief="flat")
        style.configure("TLabel", background=self.COLOR_BG, foreground=self.COLOR_TEXT, font=("Segoe UI", 9))
        style.configure("Card.TLabel", background=self.COLOR_CARD, foreground=self.COLOR_TEXT, font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=self.COLOR_BG, foreground=self.COLOR_PRIMARY, font=("Segoe UI", 15, "bold"))
        style.configure("TLabelFrame", background=self.COLOR_CARD, borderwidth=1, relief="solid")
        style.configure("TLabelFrame.Label", background=self.COLOR_CARD, foreground=self.COLOR_PRIMARY, font=("Segoe UI", 10, "bold"))

        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=7)
        style.configure("Primary.TButton", background=self.COLOR_ACCENT, foreground="white")
        style.map("Primary.TButton", background=[("active", self.COLOR_SECONDARY)])
        style.configure("Danger.TButton", background=self.COLOR_DANGER, foreground="white")
        style.map("Danger.TButton", background=[("active", "#922B21")])

        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9), background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#D9E6F2", foreground=self.COLOR_TEXT)
        style.map("Treeview", background=[("selected", self.COLOR_ACCENT)], foreground=[("selected", "white")])

    def crear_interfaz(self):
        self.crear_encabezado()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=12)

        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_productos = ttk.Frame(self.notebook)
        self.tab_stock = ttk.Frame(self.notebook)
        self.tab_ventas = ttk.Frame(self.notebook)
        self.tab_reportes = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text="📊 Dashboard")
        self.notebook.add(self.tab_productos, text="📦 Productos")
        self.notebook.add(self.tab_stock, text="🔄 Stock")
        self.notebook.add(self.tab_ventas, text="🛒 Ventas")
        self.notebook.add(self.tab_reportes, text="📋 Reportes")

        self.crear_tab_dashboard()
        self.crear_tab_productos()
        self.crear_tab_stock()
        self.crear_tab_ventas()
        self.crear_tab_reportes()

    def crear_encabezado(self):
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=78)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="MiniMarket Express",
            bg=self.COLOR_PRIMARY,
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(side="left", padx=22)

        tk.Label(
            header,
            text="Sistema PRO de Gestión de Inventario | Python + Tkinter + JSON",
            bg=self.COLOR_PRIMARY,
            fg="#D6EAF8",
            font=("Segoe UI", 10)
        ).pack(side="left", padx=5)

        self.lbl_fecha_header = tk.Label(
            header,
            text=date.today().strftime(self.FORMATO_FECHA),
            bg=self.COLOR_PRIMARY,
            fg="white",
            font=("Segoe UI", 11, "bold")
        )
        self.lbl_fecha_header.pack(side="right", padx=22)

    # ------------------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------------------
    def crear_tab_dashboard(self):
        cont = ttk.Frame(self.tab_dashboard)
        cont.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(cont, text="Panel de control", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        cards = ttk.Frame(cont)
        cards.pack(fill="x", pady=(0, 12))

        self.card_productos = self.crear_card(cards, "Total productos", "0", "📦", self.COLOR_ACCENT)
        self.card_stock_bajo = self.crear_card(cards, "Bajo stock", "0", "⚠️", self.COLOR_WARNING)
        self.card_vencer = self.crear_card(cards, "Próximos a vencer", "0", "⏳", self.COLOR_DANGER)
        self.card_ventas_dia = self.crear_card(cards, "Ventas del día", "S/ 0.00", "🛒", self.COLOR_SUCCESS)

        for card in [self.card_productos["frame"], self.card_stock_bajo["frame"], self.card_vencer["frame"], self.card_ventas_dia["frame"]]:
            card.pack(side="left", fill="x", expand=True, padx=6)

        cuerpo = ttk.Frame(cont)
        cuerpo.pack(fill="both", expand=True)

        izquierda = ttk.LabelFrame(cuerpo, text="Alertas importantes")
        izquierda.pack(side="left", fill="both", expand=True, padx=(0, 6))

        derecha = ttk.LabelFrame(cuerpo, text="Últimas ventas registradas")
        derecha.pack(side="left", fill="both", expand=True, padx=(6, 0))

        cols_alertas = ("tipo", "codigo", "producto", "detalle")
        self.tabla_alertas = ttk.Treeview(izquierda, columns=cols_alertas, show="headings", height=14)
        for col, titulo, ancho in [
            ("tipo", "Alerta", 100),
            ("codigo", "Código", 90),
            ("producto", "Producto", 210),
            ("detalle", "Detalle", 230),
        ]:
            self.tabla_alertas.heading(col, text=titulo)
            self.tabla_alertas.column(col, width=ancho, anchor="center")
        self.tabla_alertas.tag_configure("danger", background="#FADBD8")
        self.tabla_alertas.tag_configure("warning", background="#FCF3CF")
        self.tabla_alertas.pack(fill="both", expand=True, padx=10, pady=10)

        cols_ventas = ("fecha", "producto", "cantidad", "total")
        self.tabla_ultimas_ventas = ttk.Treeview(derecha, columns=cols_ventas, show="headings", height=14)
        for col, titulo, ancho in [
            ("fecha", "Fecha", 140),
            ("producto", "Producto", 230),
            ("cantidad", "Cant.", 80),
            ("total", "Total", 100),
        ]:
            self.tabla_ultimas_ventas.heading(col, text=titulo)
            self.tabla_ultimas_ventas.column(col, width=ancho, anchor="center")
        self.tabla_ultimas_ventas.pack(fill="both", expand=True, padx=10, pady=10)

    def crear_card(self, parent, titulo, valor, icono, color):
        frame = tk.Frame(parent, bg=self.COLOR_CARD, highlightbackground="#D6DBDF", highlightthickness=1, padx=12, pady=12)
        tk.Label(frame, text=icono, bg=self.COLOR_CARD, fg=color, font=("Segoe UI", 22)).pack(anchor="w")
        lbl_valor = tk.Label(frame, text=valor, bg=self.COLOR_CARD, fg=color, font=("Segoe UI", 22, "bold"))
        lbl_valor.pack(anchor="w")
        tk.Label(frame, text=titulo, bg=self.COLOR_CARD, fg="#566573", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        return {"frame": frame, "valor": lbl_valor}

    # ------------------------------------------------------------------
    # PRODUCTOS
    # ------------------------------------------------------------------
    def crear_tab_productos(self):
        cont = ttk.Frame(self.tab_productos)
        cont.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(cont, text="Gestión de productos", style="Title.TLabel").pack(anchor="w", pady=(0, 10))
        form = ttk.LabelFrame(cont, text="Datos del producto")
        form.pack(fill="x", pady=5)

        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()
        self.var_stock_min = tk.StringVar()
        self.var_vencimiento = tk.StringVar()
        self.var_buscar = tk.StringVar()

        campos = [
            ("Código", self.var_codigo),
            ("Nombre", self.var_nombre),
            ("Categoría", self.var_categoria),
            ("Precio venta", self.var_precio),
            ("Stock actual", self.var_stock),
            ("Stock mínimo", self.var_stock_min),
            ("Vencimiento DD/MM/AAAA", self.var_vencimiento),
        ]
        for i, (texto, variable) in enumerate(campos):
            fila = i // 4
            col = (i % 4) * 2
            ttk.Label(form, text=texto + ":", style="Card.TLabel").grid(row=fila, column=col, padx=8, pady=9, sticky="w")
            ttk.Entry(form, textvariable=variable, width=24).grid(row=fila, column=col + 1, padx=8, pady=9)

        botones = ttk.Frame(cont)
        botones.pack(fill="x", pady=8)
        ttk.Button(botones, text="Registrar", style="Primary.TButton", command=self.registrar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Editar", command=self.editar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar", style="Danger.TButton", command=self.eliminar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_producto).pack(side="left", padx=5)
        ttk.Label(botones, text="Buscar:").pack(side="left", padx=(30, 5))
        ttk.Entry(botones, textvariable=self.var_buscar, width=35).pack(side="left", padx=5)
        ttk.Button(botones, text="Buscar", command=self.buscar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Mostrar todos", command=self.cargar_productos).pack(side="left", padx=5)

        cols = ("codigo", "nombre", "categoria", "precio", "stock", "stock_minimo", "vencimiento", "estado")
        self.tabla_productos = ttk.Treeview(cont, columns=cols, show="headings")
        titulos = ["Código", "Nombre", "Categoría", "Precio", "Stock", "Stock mínimo", "Vencimiento", "Estado"]
        anchos = [100, 190, 150, 90, 80, 110, 120, 130]
        for col, titulo, ancho in zip(cols, titulos, anchos):
            self.tabla_productos.heading(col, text=titulo)
            self.tabla_productos.column(col, width=ancho, anchor="center")
        self.tabla_productos.tag_configure("bajo", background="#FADBD8")
        self.tabla_productos.tag_configure("ok", background="#EAF2F8")
        self.tabla_productos.pack(fill="both", expand=True)
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    def validar_producto(self):
        codigo = self.var_codigo.get().strip()
        nombre = self.var_nombre.get().strip()
        categoria = self.var_categoria.get().strip()
        precio = self.var_precio.get().strip()
        stock = self.var_stock.get().strip()
        stock_min = self.var_stock_min.get().strip()
        vencimiento = self.var_vencimiento.get().strip()

        if not codigo or not nombre or not categoria or not precio or not stock or not stock_min:
            raise ValueError("Complete los campos importantes.")
        try:
            precio = float(precio)
            stock = int(stock)
            stock_min = int(stock_min)
            if precio < 0 or stock < 0 or stock_min < 0:
                raise ValueError
        except ValueError:
            raise ValueError("Precio, stock y stock mínimo deben ser numéricos positivos.")
        if vencimiento:
            try:
                datetime.strptime(vencimiento, self.FORMATO_FECHA)
            except ValueError:
                raise ValueError("La fecha de vencimiento debe tener formato DD/MM/AAAA. Ejemplo: 06/05/2026")
        return Producto(codigo, nombre, categoria, precio, stock, stock_min, vencimiento).to_dict()

    def registrar_producto(self):
        try:
            self.producto_service.registrar(self.validar_producto())
            messagebox.showinfo("Correcto", "Producto registrado correctamente.")
            self.limpiar_producto()
            self.refrescar_todo()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))

    def editar_producto(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione o ingrese un código de producto.")
            return
        try:
            datos = self.validar_producto()
            self.producto_service.editar(codigo, datos)
            messagebox.showinfo("Correcto", "Producto editado correctamente.")
            self.refrescar_todo()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))

    def eliminar_producto(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione un producto.")
            return
        if messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar este producto del inventario?"):
            try:
                self.producto_service.eliminar(codigo)
                self.limpiar_producto()
                self.refrescar_todo()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def seleccionar_producto(self, _event=None):
        item = self.tabla_productos.selection()
        if not item:
            return
        valores = self.tabla_productos.item(item[0], "values")
        self.var_codigo.set(valores[0])
        self.var_nombre.set(valores[1])
        self.var_categoria.set(valores[2])
        self.var_precio.set(valores[3])
        self.var_stock.set(valores[4])
        self.var_stock_min.set(valores[5])
        self.var_vencimiento.set(valores[6])

    def limpiar_producto(self):
        for var in [self.var_codigo, self.var_nombre, self.var_categoria, self.var_precio, self.var_stock, self.var_stock_min, self.var_vencimiento]:
            var.set("")

    def buscar_producto(self):
        self.cargar_productos(self.producto_service.buscar(self.var_buscar.get()))

    def cargar_productos(self, productos=None):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        productos = productos if productos is not None else self.producto_service.listar()
        for p in productos:
            estado = "BAJO STOCK" if int(p["stock"]) <= int(p["stock_minimo"]) else "OK"
            tag = "bajo" if estado == "BAJO STOCK" else "ok"
            self.tabla_productos.insert("", "end", values=(
                p["codigo"], p["nombre"], p["categoria"], f'{float(p["precio"]):.2f}',
                p["stock"], p["stock_minimo"], p.get("vencimiento", ""), estado
            ), tags=(tag,))

    # ------------------------------------------------------------------
    # STOCK
    # ------------------------------------------------------------------
    def crear_tab_stock(self):
        cont = ttk.Frame(self.tab_stock)
        cont.pack(fill="both", expand=True, padx=12, pady=12)
        ttk.Label(cont, text="Movimientos de stock", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        form = ttk.LabelFrame(cont, text="Registrar ingreso o salida de mercadería")
        form.pack(fill="x", pady=5)

        self.var_stock_producto = tk.StringVar()
        self.var_stock_cantidad = tk.StringVar()
        self.var_stock_tipo = tk.StringVar(value="INGRESO")
        self.var_stock_motivo = tk.StringVar()

        ttk.Label(form, text="Producto:", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=9)
        self.combo_stock_producto = ttk.Combobox(form, textvariable=self.var_stock_producto, width=48, state="readonly")
        self.combo_stock_producto.grid(row=0, column=1, padx=8, pady=9)
        ttk.Label(form, text="Cantidad:", style="Card.TLabel").grid(row=0, column=2, padx=8, pady=9)
        ttk.Entry(form, textvariable=self.var_stock_cantidad, width=15).grid(row=0, column=3, padx=8, pady=9)
        ttk.Label(form, text="Tipo:", style="Card.TLabel").grid(row=0, column=4, padx=8, pady=9)
        ttk.Combobox(form, textvariable=self.var_stock_tipo, values=["INGRESO", "SALIDA"], state="readonly", width=12).grid(row=0, column=5, padx=8, pady=9)
        ttk.Label(form, text="Motivo:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=9)
        ttk.Entry(form, textvariable=self.var_stock_motivo, width=58).grid(row=1, column=1, columnspan=2, padx=8, pady=9)
        ttk.Button(form, text="Registrar movimiento", style="Primary.TButton", command=self.registrar_movimiento_stock).grid(row=1, column=3, padx=8, pady=9)

        cols = ("fecha", "codigo", "producto", "tipo", "cantidad", "stock", "motivo")
        self.tabla_movimientos = ttk.Treeview(cont, columns=cols, show="headings")
        titulos = ["Fecha", "Código", "Producto", "Tipo", "Cantidad", "Stock final", "Motivo"]
        for col, titulo in zip(cols, titulos):
            self.tabla_movimientos.heading(col, text=titulo)
            self.tabla_movimientos.column(col, width=145, anchor="center")
        self.tabla_movimientos.tag_configure("ingreso", background="#D5F5E3")
        self.tabla_movimientos.tag_configure("salida", background="#FDEDEC")
        self.tabla_movimientos.pack(fill="both", expand=True, pady=(8, 0))

    def registrar_movimiento_stock(self):
        try:
            codigo = self.extraer_codigo_combo(self.var_stock_producto.get())
            cantidad = int(self.var_stock_cantidad.get())
            motivo = self.var_stock_motivo.get().strip() or "Movimiento manual"
            producto = self.stock_service.mover_stock(codigo, cantidad, self.var_stock_tipo.get(), motivo)
            if producto["stock"] <= producto["stock_minimo"]:
                messagebox.showwarning("Alerta de stock", f'El producto {producto["nombre"]} está en bajo stock.')
            else:
                messagebox.showinfo("Correcto", "Movimiento registrado correctamente.")
            self.var_stock_cantidad.set("")
            self.var_stock_motivo.set("")
            self.refrescar_todo()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cargar_movimientos(self):
        for item in self.tabla_movimientos.get_children():
            self.tabla_movimientos.delete(item)
        for m in reversed(self.stock_service.listar_movimientos()):
            tag = "ingreso" if m["tipo"] == "INGRESO" else "salida"
            self.tabla_movimientos.insert("", "end", values=(m["fecha"], m["codigo"], m["producto"], m["tipo"], m["cantidad"], m["stock_resultante"], m["motivo"]), tags=(tag,))

    # ------------------------------------------------------------------
    # VENTAS
    # ------------------------------------------------------------------
    def crear_tab_ventas(self):
        cont = ttk.Frame(self.tab_ventas)
        cont.pack(fill="both", expand=True, padx=12, pady=12)
        ttk.Label(cont, text="Registro de ventas", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        form = ttk.LabelFrame(cont, text="Nueva venta")
        form.pack(fill="x", pady=5)

        self.var_venta_producto = tk.StringVar()
        self.var_venta_cantidad = tk.StringVar()
        self.var_venta_total = tk.StringVar(value="0.00")

        ttk.Label(form, text="Producto:", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=9)
        self.combo_venta_producto = ttk.Combobox(form, textvariable=self.var_venta_producto, width=48, state="readonly")
        self.combo_venta_producto.grid(row=0, column=1, padx=8, pady=9)
        ttk.Label(form, text="Cantidad:", style="Card.TLabel").grid(row=0, column=2, padx=8, pady=9)
        ttk.Entry(form, textvariable=self.var_venta_cantidad, width=15).grid(row=0, column=3, padx=8, pady=9)
        ttk.Button(form, text="Calcular total", command=self.calcular_total_venta).grid(row=0, column=4, padx=8, pady=9)
        ttk.Label(form, text="Total S/:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=9)
        tk.Label(form, textvariable=self.var_venta_total, bg=self.COLOR_CARD, fg=self.COLOR_SUCCESS, font=("Segoe UI", 16, "bold")).grid(row=1, column=1, padx=8, pady=9, sticky="w")
        ttk.Button(form, text="Registrar venta", style="Primary.TButton", command=self.registrar_venta).grid(row=1, column=2, padx=8, pady=9)

        cols = ("fecha", "codigo", "producto", "cantidad", "precio", "total")
        self.tabla_ventas = ttk.Treeview(cont, columns=cols, show="headings")
        titulos = ["Fecha", "Código", "Producto", "Cantidad", "Precio", "Total"]
        for col, titulo in zip(cols, titulos):
            self.tabla_ventas.heading(col, text=titulo)
            self.tabla_ventas.column(col, width=155, anchor="center")
        self.tabla_ventas.pack(fill="both", expand=True, pady=(8, 0))

    def calcular_total_venta(self):
        try:
            codigo = self.extraer_codigo_combo(self.var_venta_producto.get())
            producto = self.producto_service.buscar_por_codigo(codigo)
            cantidad = int(self.var_venta_cantidad.get())
            if not producto or cantidad <= 0:
                raise ValueError
            if cantidad > int(producto["stock"]):
                raise ValueError("No se puede vender más stock del disponible.")
            self.var_venta_total.set(f'{float(producto["precio"]) * cantidad:.2f}')
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e) else "Seleccione un producto e ingrese una cantidad válida.")

    def registrar_venta(self):
        try:
            codigo = self.extraer_codigo_combo(self.var_venta_producto.get())
            cantidad = int(self.var_venta_cantidad.get())
            venta = self.venta_service.registrar_venta(codigo, cantidad)
            messagebox.showinfo("Correcto", f'Venta registrada. Total: S/ {venta["total"]:.2f}')
            self.var_venta_cantidad.set("")
            self.var_venta_total.set("0.00")
            self.refrescar_todo()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cargar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        for v in reversed(self.venta_service.listar()):
            self.tabla_ventas.insert("", "end", values=(v["fecha"], v["codigo"], v["producto"], v["cantidad"], f'{float(v["precio_unitario"]):.2f}', f'{float(v["total"]):.2f}'))

    # ------------------------------------------------------------------
    # REPORTES
    # ------------------------------------------------------------------
    def crear_tab_reportes(self):
        cont = ttk.Frame(self.tab_reportes)
        cont.pack(fill="both", expand=True, padx=12, pady=12)
        ttk.Label(cont, text="Reportes básicos", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        botones = ttk.Frame(cont)
        botones.pack(fill="x", pady=8)
        ttk.Button(botones, text="Bajo stock", command=self.reporte_bajo_stock).pack(side="left", padx=5)
        ttk.Button(botones, text="Próximos a vencer", command=self.reporte_vencimiento).pack(side="left", padx=5)
        ttk.Button(botones, text="Ventas del día", command=self.reporte_ventas_dia).pack(side="left", padx=5)
        ttk.Button(botones, text="Más vendidos", command=self.reporte_mas_vendidos).pack(side="left", padx=5)
        ttk.Button(botones, text="Stock general", command=self.reporte_stock_general).pack(side="left", padx=5)

        self.texto_reporte = tk.Text(cont, font=("Consolas", 10), wrap="word", bg="white", fg=self.COLOR_TEXT, relief="solid", bd=1)
        self.texto_reporte.pack(fill="both", expand=True)

    def mostrar_reporte(self, titulo, lineas):
        self.texto_reporte.delete("1.0", "end")
        self.texto_reporte.insert("end", titulo + "\n")
        self.texto_reporte.insert("end", "=" * len(titulo) + "\n\n")
        if not lineas:
            self.texto_reporte.insert("end", "No hay datos para mostrar.\n")
            return
        for linea in lineas:
            self.texto_reporte.insert("end", linea + "\n")

    def reporte_bajo_stock(self):
        datos = [f'{p["codigo"]} | {p["nombre"]} | Stock: {p["stock"]} | Mínimo: {p["stock_minimo"]}' for p in self.reporte_service.bajo_stock()]
        self.mostrar_reporte("PRODUCTOS CON BAJO STOCK", datos)

    def reporte_vencimiento(self):
        datos = [f'{p["codigo"]} | {p["nombre"]} | Vence: {p.get("vencimiento", "")}' for p in self.reporte_service.proximos_a_vencer()]
        self.mostrar_reporte("PRODUCTOS PRÓXIMOS A VENCER", datos)

    def reporte_ventas_dia(self):
        ventas = self.reporte_service.ventas_del_dia()
        datos = [f'{v["fecha"]} | {v["producto"]} | Cant: {v["cantidad"]} | Total: S/ {float(v["total"]):.2f}' for v in ventas]
        total = sum(float(v["total"]) for v in ventas)
        datos.append(f"\nTOTAL VENDIDO DEL DÍA: S/ {total:.2f}")
        self.mostrar_reporte("VENTAS DEL DÍA", datos)

    def reporte_mas_vendidos(self):
        datos = [f'{codigo} | {info["producto"]} | Cantidad vendida: {info["cantidad"]} | Total: S/ {info["total"]:.2f}' for codigo, info in self.reporte_service.productos_mas_vendidos()]
        self.mostrar_reporte("PRODUCTOS MÁS VENDIDOS", datos)

    def reporte_stock_general(self):
        datos = [f'{p["codigo"]} | {p["nombre"]} | Categoría: {p["categoria"]} | Stock: {p["stock"]} | Precio: S/ {float(p["precio"]):.2f}' for p in self.reporte_service.stock_general()]
        self.mostrar_reporte("STOCK GENERAL", datos)

    # ------------------------------------------------------------------
    # UTILIDADES Y ACTUALIZACIONES
    # ------------------------------------------------------------------
    def actualizar_dashboard(self):
        productos = self.producto_service.listar()
        bajo_stock = self.reporte_service.bajo_stock()
        proximos = self.reporte_service.proximos_a_vencer()
        ventas_dia = self.reporte_service.ventas_del_dia()
        total_dia = sum(float(v["total"]) for v in ventas_dia)

        self.card_productos["valor"].config(text=str(len(productos)))
        self.card_stock_bajo["valor"].config(text=str(len(bajo_stock)))
        self.card_vencer["valor"].config(text=str(len(proximos)))
        self.card_ventas_dia["valor"].config(text=f"S/ {total_dia:.2f}")

        for item in self.tabla_alertas.get_children():
            self.tabla_alertas.delete(item)
        for p in bajo_stock:
            self.tabla_alertas.insert("", "end", values=("Stock", p["codigo"], p["nombre"], f'Stock {p["stock"]} / Mínimo {p["stock_minimo"]}'), tags=("danger",))
        for p in proximos:
            self.tabla_alertas.insert("", "end", values=("Vence", p["codigo"], p["nombre"], f'Vence {p.get("vencimiento", "")}'), tags=("warning",))

        for item in self.tabla_ultimas_ventas.get_children():
            self.tabla_ultimas_ventas.delete(item)
        for v in list(reversed(self.venta_service.listar()))[:10]:
            self.tabla_ultimas_ventas.insert("", "end", values=(v["fecha"], v["producto"], v["cantidad"], f'S/ {float(v["total"]):.2f}'))

    def actualizar_combos(self):
        valores = [f'{p["codigo"]} - {p["nombre"]}' for p in self.producto_service.listar()]
        self.combo_stock_producto["values"] = valores
        self.combo_venta_producto["values"] = valores

    def extraer_codigo_combo(self, valor):
        if not valor or " - " not in valor:
            raise ValueError("Seleccione un producto.")
        return valor.split(" - ")[0]

    def refrescar_todo(self):
        self.cargar_productos()
        self.cargar_movimientos()
        self.cargar_ventas()
        self.actualizar_combos()
        self.actualizar_dashboard()
        self.reporte_stock_general()
