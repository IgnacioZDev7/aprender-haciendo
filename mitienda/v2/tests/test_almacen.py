import csv

import pytest

from mitienda import almacen


def test_registrar_venta_descuenta_stock(con):
    almacen.registrar_venta(con, {"pan": 10, "queso": 3}, fecha="2026-11-16 09:00")
    assert almacen.buscar_producto(con, "pan")["stock"] == 90
    assert almacen.buscar_producto(con, "queso")["stock"] == 2


def test_total_del_dia_aplica_descuento(con):
    # 10 x 0.5 + 3 x 45 = 140 -> 5 % de descuento -> 133
    almacen.registrar_venta(con, {"pan": 10, "queso": 3}, fecha="2026-11-16 09:00")
    assert almacen.total_del_dia(con, "2026-11-16") == 133.0
    assert almacen.total_del_dia(con, "2026-11-17") == 0


def test_no_vende_mas_que_el_stock(con):
    with pytest.raises(almacen.ErrorDeVenta, match="Solo hay 5"):
        almacen.registrar_venta(con, {"queso": 6})
    # La venta fallida no dejó rastros
    assert almacen.buscar_producto(con, "queso")["stock"] == 5
    assert con.execute("SELECT COUNT(*) FROM ventas").fetchone()[0] == 0


def test_producto_inexistente(con):
    with pytest.raises(almacen.ErrorDeVenta, match="no está en el catálogo"):
        almacen.registrar_venta(con, {"fideo": 1})


def test_anular_venta_devuelve_stock(con):
    venta = almacen.registrar_venta(con, {"queso": 2}, fecha="2026-11-16 10:00")
    assert almacen.anular_venta(con, venta)
    assert almacen.buscar_producto(con, "queso")["stock"] == 5
    assert almacen.total_del_dia(con, "2026-11-16") == 0
    assert not almacen.anular_venta(con, venta)  # no se anula dos veces


def test_actualizar_precio(con):
    assert almacen.actualizar_precio(con, "Pan", 0.6)
    assert almacen.buscar_producto(con, "pan")["precio"] == 0.6
    assert not almacen.actualizar_precio(con, "fideo", 3)


def test_productos_para_reponer(con):
    nombres = [p["nombre"] for p in almacen.productos_para_reponer(con)]
    assert nombres == ["queso"]


def test_exportar_mes(con, tmp_path):
    almacen.registrar_venta(con, {"pan": 4}, fecha="2026-11-16 09:00")
    almacen.registrar_venta(con, {"pan": 2}, fecha="2026-12-01 09:00")
    ruta = tmp_path / "noviembre.csv"
    assert almacen.exportar_mes(con, "2026-11", ruta) == 1
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.reader(f))
    assert filas == [
        ["fecha", "producto", "cantidad", "importe"],
        ["2026-11-16 09:00", "pan", "4", "2.0"],
    ]


def test_nombre_con_comilla_no_rompe_la_consulta(con):
    # Las consultas con ? tratan el texto como dato, no como SQL
    assert almacen.buscar_producto(con, "pan' OR '1'='1") is None
