# MiTienda v2

Sistema de ventas para una tienda de barrio: catálogo con stock, ventas de varios productos con descuento automático, anulación de ventas, reporte del día y exportación mensual a CSV. Es el proyecto del Libro 2, *Del programa al producto*.

## Instalación

```
pip install .
```

## Uso

```
mitienda          # o: python -m mitienda
```

Los datos se guardan en `mitienda.db` (SQLite) en la carpeta actual. La primera vez se carga un catálogo de ejemplo.

## Desarrollo

```
pip install -e ".[dev]"
pytest --cov=mitienda
ruff check .
ruff format .
```

## Estructura

| Módulo | Capa | Responsabilidad |
|---|---|---|
| `mitienda/reglas.py` | Reglas del negocio | Descuentos y stock mínimo (funciones puras) |
| `mitienda/almacen.py` | Datos | SQLite: productos, ventas, reportes |
| `mitienda/cli.py` | Presentación | Menú de consola |

## Estado de las historias

| Historia | Estado |
|---|---|
| HU-01 Venta de varios productos | Terminada |
| HU-02 Total vendido en el día | Terminada |
| HU-03 Editar catálogo | En curso: funciones listas, falta la opción de menú |
| HU-04 Productos para reponer | Terminada |
| HU-05 Anular una venta | Terminada |
| HU-06 Exportar ventas del mes | Terminada |
