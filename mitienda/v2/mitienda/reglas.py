"""Reglas de negocio de MiTienda. Funciones puras: no leen ni escriben datos."""

UMBRAL_DESCUENTO_ALTO = 200
UMBRAL_DESCUENTO_MEDIO = 100
DESCUENTO_ALTO = 10
DESCUENTO_MEDIO = 5
STOCK_MINIMO = 10


def calcular_descuento(subtotal: float) -> int:
    """Porcentaje de descuento que corresponde a un subtotal."""
    if subtotal > UMBRAL_DESCUENTO_ALTO:
        return DESCUENTO_ALTO
    if subtotal > UMBRAL_DESCUENTO_MEDIO:
        return DESCUENTO_MEDIO
    return 0


def aplicar_descuento(monto: float, porcentaje: int) -> float:
    """Monto con el porcentaje de descuento aplicado, redondeado a 2 decimales."""
    return round(monto * (1 - porcentaje / 100), 2)


def necesita_reposicion(stock: int, minimo: int = STOCK_MINIMO) -> bool:
    """True si el stock es menor que el mínimo (HU-04)."""
    return stock < minimo
