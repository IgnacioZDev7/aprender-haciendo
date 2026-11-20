"""Acceso a datos de MiTienda con SQLite (capítulo 8 del Libro 2)."""

import csv
import sqlite3
from datetime import datetime

from mitienda import reglas

ESQUEMA = """
CREATE TABLE IF NOT EXISTS productos (
    id      INTEGER PRIMARY KEY,
    nombre  TEXT    NOT NULL UNIQUE,
    precio  REAL    NOT NULL CHECK (precio > 0),
    stock   INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);
CREATE TABLE IF NOT EXISTS ventas (
    id      INTEGER PRIMARY KEY,
    fecha   TEXT    NOT NULL,
    total   REAL    NOT NULL,
    anulada INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS lineas_venta (
    venta_id    INTEGER NOT NULL REFERENCES ventas(id),
    producto_id INTEGER NOT NULL REFERENCES productos(id),
    cantidad    INTEGER NOT NULL CHECK (cantidad > 0),
    importe     REAL    NOT NULL
);
"""


class ErrorDeVenta(Exception):
    """Una venta no se puede registrar (producto inexistente, sin stock, etc.)."""


def conectar(ruta: str = "mitienda.db") -> sqlite3.Connection:
    """Abre la base de datos y crea las tablas si no existen."""
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.executescript(ESQUEMA)
    return conexion


# ---------- Catálogo (HU-03) ----------


def agregar_producto(con, nombre: str, precio: float, stock: int = 0) -> int:
    with con:
        cursor = con.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre.strip().lower(), precio, stock),
        )
    return cursor.lastrowid


def actualizar_precio(con, nombre: str, nuevo_precio: float) -> bool:
    with con:
        cursor = con.execute(
            "UPDATE productos SET precio = ? WHERE nombre = ?",
            (nuevo_precio, nombre.strip().lower()),
        )
    return cursor.rowcount == 1


def buscar_producto(con, nombre: str):
    return con.execute(
        "SELECT * FROM productos WHERE nombre = ?", (nombre.strip().lower(),)
    ).fetchone()


def listar_productos(con):
    return con.execute("SELECT * FROM productos ORDER BY nombre").fetchall()


# ---------- Ventas (HU-01, HU-05) ----------


def registrar_venta(con, pedido: dict[str, int], fecha: str | None = None) -> int:
    """Registra una venta de varios productos y descuenta el stock.

    pedido: {nombre_producto: cantidad}. Devuelve el id de la venta.
    Si algún producto no existe o no tiene stock, no se guarda nada.
    """
    if not pedido:
        raise ErrorDeVenta("La venta no tiene productos")
    fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M")
    lineas = []
    for nombre, cantidad in pedido.items():
        producto = buscar_producto(con, nombre)
        if producto is None:
            raise ErrorDeVenta(f"'{nombre}' no está en el catálogo")
        if cantidad <= 0:
            raise ErrorDeVenta(f"Cantidad inválida para '{nombre}'")
        if cantidad > producto["stock"]:
            raise ErrorDeVenta(
                f"Solo hay {producto['stock']} unidades de '{producto['nombre']}'"
            )
        lineas.append((producto, cantidad, producto["precio"] * cantidad))

    subtotal = sum(importe for _, _, importe in lineas)
    porcentaje = reglas.calcular_descuento(subtotal)
    total = reglas.aplicar_descuento(subtotal, porcentaje)

    with con:  # transacción: o se guarda todo, o nada
        venta_id = con.execute(
            "INSERT INTO ventas (fecha, total) VALUES (?, ?)", (fecha, total)
        ).lastrowid
        for producto, cantidad, importe in lineas:
            con.execute(
                "INSERT INTO lineas_venta (venta_id, producto_id, cantidad, importe)"
                " VALUES (?, ?, ?, ?)",
                (
                    venta_id,
                    producto["id"],
                    cantidad,
                    reglas.aplicar_descuento(importe, porcentaje),
                ),
            )
            con.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (cantidad, producto["id"]),
            )
    return venta_id


def anular_venta(con, venta_id: int) -> bool:
    """Marca una venta como anulada y devuelve el stock (HU-05)."""
    venta = con.execute(
        "SELECT anulada FROM ventas WHERE id = ?", (venta_id,)
    ).fetchone()
    if venta is None or venta["anulada"]:
        return False
    with con:
        con.execute("UPDATE ventas SET anulada = 1 WHERE id = ?", (venta_id,))
        con.execute(
            """UPDATE productos SET stock = stock + (
                   SELECT cantidad FROM lineas_venta
                   WHERE venta_id = ? AND producto_id = productos.id)
               WHERE id IN (SELECT producto_id FROM lineas_venta WHERE venta_id = ?)""",
            (venta_id, venta_id),
        )
    return True


# ---------- Reportes (HU-02, HU-04, HU-06) ----------


def total_del_dia(con, dia: str) -> float:
    """Total vendido en un día 'AAAA-MM-DD', sin contar ventas anuladas."""
    fila = con.execute(
        "SELECT COALESCE(SUM(total), 0) FROM ventas WHERE fecha LIKE ? AND anulada = 0",
        (dia + "%",),
    ).fetchone()
    return round(fila[0], 2)


def productos_para_reponer(con, minimo: int = reglas.STOCK_MINIMO):
    return [
        p
        for p in listar_productos(con)
        if reglas.necesita_reposicion(p["stock"], minimo)
    ]


def exportar_mes(con, mes: str, ruta_csv: str) -> int:
    """Exporta a CSV las líneas de venta de un mes 'AAAA-MM'. Devuelve las filas."""
    filas = con.execute(
        """SELECT v.fecha, p.nombre, l.cantidad, l.importe
           FROM lineas_venta l
           JOIN ventas v    ON v.id = l.venta_id
           JOIN productos p ON p.id = l.producto_id
           WHERE v.fecha LIKE ? AND v.anulada = 0
           ORDER BY v.fecha""",
        (mes + "%",),
    ).fetchall()
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["fecha", "producto", "cantidad", "importe"])
        escritor.writerows([tuple(fila) for fila in filas])
    return len(filas)
