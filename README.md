# Aprender Haciendo

[![Pruebas de MiTienda](https://github.com/IgnacioZDev7/aprender-haciendo/actions/workflows/pruebas.yml/badge.svg)](https://github.com/IgnacioZDev7/aprender-haciendo/actions/workflows/pruebas.yml)
[![Publicar los libros](https://github.com/IgnacioZDev7/aprender-haciendo/actions/workflows/publicar-libros.yml/badge.svg)](https://github.com/IgnacioZDev7/aprender-haciendo/actions/workflows/publicar-libros.yml)

Serie de dos manuales prácticos de programación para estudiantes universitarios, escrita por Ignacio Zárate a partir de su experiencia como ayudante de cátedra.

| Libro | Para quién | Leer |
|---|---|---|
| **1. Programar desde cero** — Lógica y Python con retos guiados | Primeros semestres | [Web](https://ignaciozdev7.github.io/aprender-haciendo/libro1/) |
| **2. Del programa al producto** — Desarrollo de software paso a paso | Nivel intermedio | [Web](https://ignaciozdev7.github.io/aprender-haciendo/libro2/) |

Cada versión web tiene un botón para descargar el PDF (A5).

Los dos libros comparten un proyecto: **MiTienda**, el sistema de ventas de la tienda de Doña Rosa. En el Libro 1 crece de pseudocódigo a un programa de consola (v1.0); en el Libro 2 se convierte en un producto en equipo (v2.0).

## Contenido del repositorio

```
libro1/          fuentes Quarto del Libro 1 (.qmd)
libro2/          fuentes Quarto del Libro 2 (.qmd)
comun/           estilo del PDF compartido por los dos libros
mitienda/v1/     MiTienda v1.0 (Libro 1) y sus pruebas
mitienda/v2/     MiTienda v2.0 (Libro 2): paquete, pruebas, pyproject.toml
portada/         página de inicio del sitio web
.github/         integración continua: pruebas y publicación de los libros
```

## Generar los libros en tu computadora

Requisitos: [Quarto](https://quarto.org/docs/get-started/) y Python 3.12+ con `pip install jupyter matplotlib`. El PDF se genera con Typst, que viene incluido en Quarto (no hace falta LaTeX).

```bash
quarto preview libro1        # vista previa web que se actualiza al guardar
quarto render libro1         # web + PDF en libro1/_book/
```

## Ejecutar MiTienda

```bash
cd mitienda/v1 && python mitienda.py            # versión del Libro 1
cd mitienda/v2 && pip install -e ".[dev]"       # versión del Libro 2
mitienda                                        # o: python -m mitienda
pytest                                          # 19 pruebas
```

## Licencias

- Texto de los libros: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es).
- Código de MiTienda: [MIT](mitienda/LICENSE).

## Uso de inteligencia artificial

Los borradores de los capítulos se prepararon con apoyo de asistentes de IA. Todo el contenido fue revisado y adaptado por el autor, todo el código se ejecutó y probó antes de incluirse, y cada referencia bibliográfica se verificó en su fuente. Los detalles están en el prólogo de cada libro.
