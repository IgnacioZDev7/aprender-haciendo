import pytest

from mitienda import reglas


@pytest.mark.parametrize(
    "subtotal, esperado",
    [(50, 0), (100, 0), (100.01, 5), (200, 5), (200.01, 10), (1000, 10)],
)
def test_calcular_descuento(subtotal, esperado):
    assert reglas.calcular_descuento(subtotal) == esperado


def test_aplicar_descuento_redondea():
    assert reglas.aplicar_descuento(140, 5) == 133.0
    assert reglas.aplicar_descuento(10, 0) == 10


def test_necesita_reposicion():
    assert reglas.necesita_reposicion(9)
    assert not reglas.necesita_reposicion(10)
