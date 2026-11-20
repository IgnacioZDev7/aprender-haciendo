import pytest

from mitienda import almacen


@pytest.fixture
def con():
    """Base de datos en memoria con un catálogo pequeño, nueva en cada prueba."""
    conexion = almacen.conectar(":memory:")
    almacen.agregar_producto(conexion, "pan", 0.5, 100)
    almacen.agregar_producto(conexion, "queso", 45.0, 5)
    yield conexion
    conexion.close()
