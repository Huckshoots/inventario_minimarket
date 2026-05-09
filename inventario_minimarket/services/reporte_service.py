from datetime import datetime, date, timedelta
from collections import defaultdict


class ReporteService:
    def __init__(self, producto_service, venta_service):
        self.producto_service = producto_service
        self.venta_service = venta_service

    def _parse_fecha(self, valor):
        if not valor:
            return None
        valor = str(valor).split()[0]
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(valor, formato).date()
            except ValueError:
                continue
        return None

    def bajo_stock(self):
        return [p for p in self.producto_service.listar() if int(p["stock"]) <= int(p["stock_minimo"])]

    def proximos_a_vencer(self, dias=30):
        resultado = []
        hoy = date.today()
        limite = hoy + timedelta(days=dias)
        for p in self.producto_service.listar():
            fecha = self._parse_fecha(p.get("vencimiento", ""))
            if fecha and hoy <= fecha <= limite:
                resultado.append(p)
        return resultado

    def ventas_del_dia(self):
        hoy = date.today()
        return [v for v in self.venta_service.listar() if self._parse_fecha(v.get("fecha", "")) == hoy]

    def productos_mas_vendidos(self):
        acumulado = defaultdict(lambda: {"producto": "", "cantidad": 0, "total": 0.0})
        for v in self.venta_service.listar():
            codigo = v["codigo"]
            acumulado[codigo]["producto"] = v["producto"]
            acumulado[codigo]["cantidad"] += int(v["cantidad"])
            acumulado[codigo]["total"] += float(v["total"])
        return sorted(acumulado.items(), key=lambda x: x[1]["cantidad"], reverse=True)

    def stock_general(self):
        return self.producto_service.listar()
