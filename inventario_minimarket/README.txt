MiniMarket Express - Sistema PRO de Inventario
================================================

Tecnologías usadas:
- Python
- Tkinter
- JSON
- Librerías estándar de Python

No usa SQLite, MySQL, PostgreSQL ni frameworks web.

Ejecución:
1. Abrir la carpeta del proyecto en Visual Studio Code.
2. Ejecutar en terminal:

   python main.py

Estructura:
- main.py: inicia el programa.
- ui/app.py: interfaz gráfica Tkinter versión PRO.
- models/: modelos de datos.
- services/: lógica de productos, stock, ventas y reportes.
- storage/json_storage.py: lectura y escritura de archivos JSON.
- data/: archivos permanentes productos.json, ventas.json y movimientos_stock.json.

Formato de fecha usado en pantalla y validación:
- DD/MM/AAAA
- Ejemplo: 06/05/2026

Mejoras de la versión PRO:
- Dashboard inicial con métricas.
- Alertas visuales para bajo stock y vencimiento.
- Colores modernos.
- Tablas con estados.
- Mejor presentación para exposición académica.
