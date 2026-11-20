"""Pruebas de MiTienda v1.0. Ejecutar con:  python test_mitienda.py
(o con pytest, que se presenta en el Libro 2)."""
import mitienda


def test_descuento_fronteras():
    assert mitienda.calcular_descuento(100) == 0
    assert mitienda.calcular_descuento(100.01) == 5
    assert mitienda.calcular_descuento(200) == 5
    assert mitienda.calcular_descuento(200.01) == 10


def test_aplicar_descuento():
    assert mitienda.aplicar_descuento(140, 5) == 133.0
    assert mitienda.aplicar_descuento(50, 0) == 50


def test_reporte():
    filas = [
        ["2026-11-16 09:00", "pan", "10", "5.0"],
        ["2026-11-16 09:05", "queso", "3", "128.25"],
        ["2026-11-16 10:00", "pan", "4", "2.0"],
    ]
    unidades = mitienda.ventas_por_producto(filas)
    assert unidades == {"pan": 14, "queso": 3}
    assert mitienda.producto_mas_vendido(unidades) == "pan"
    assert mitienda.total_vendido(filas) == 135.25
    assert mitienda.producto_mas_vendido({}) is None


if __name__ == "__main__":
    test_descuento_fronteras()
    test_aplicar_descuento()
    test_reporte()
    print("¡Todas las pruebas pasaron!")
