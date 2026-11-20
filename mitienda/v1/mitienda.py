"""MiTienda v1.0: programa de ventas para la tienda de Doña Rosa.

Proyecto final del Libro 1 de la serie «Aprender Haciendo».
Ejecutar con:  python mitienda.py
"""
import csv
from datetime import datetime

ARCHIVO_VENTAS = "ventas.csv"
CATALOGO = {"pan": 0.5, "leche": 6.0, "queso": 45.0, "arroz": 9.5}


# ---------- Cálculos (sin input ni print: se pueden probar) ----------

def calcular_descuento(subtotal):
    """Porcentaje de descuento según el subtotal de la compra."""
    if subtotal > 200:
        return 10
    elif subtotal > 100:
        return 5
    return 0


def aplicar_descuento(subtotal, porcentaje):
    """Subtotal con el descuento aplicado, redondeado a 2 decimales."""
    return round(subtotal * (1 - porcentaje / 100), 2)


def ventas_por_producto(filas):
    """Recibe filas [fecha, producto, cantidad, importe] y devuelve
    un diccionario {producto: unidades vendidas}."""
    unidades = {}
    for fila in filas:
        producto, cantidad = fila[1], int(fila[2])
        unidades[producto] = unidades.get(producto, 0) + cantidad
    return unidades


def producto_mas_vendido(unidades):
    """Producto con más unidades vendidas, o None si no hay ventas."""
    if not unidades:
        return None
    return max(unidades, key=unidades.get)


# ---------- Archivo de ventas ----------

def guardar_venta(producto, cantidad, importe):
    """Agrega una línea al archivo de ventas (no borra las anteriores)."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(ARCHIVO_VENTAS, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([fecha, producto, cantidad, importe])


def leer_ventas():
    """Devuelve la lista de filas guardadas; vacía si aún no hay archivo."""
    try:
        with open(ARCHIVO_VENTAS, newline="", encoding="utf-8") as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return []


def total_vendido(filas):
    """Suma de la columna de importes."""
    return round(sum(float(fila[3]) for fila in filas), 2)


# ---------- Conversación con el usuario ----------

def pedir_entero(mensaje, minimo=1):
    """Pide un entero mayor o igual que minimo; insiste hasta obtenerlo."""
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Escribe un número entero, por ejemplo 3")
            continue
        if numero >= minimo:
            return numero
        print(f"Debe ser mayor o igual que {minimo}")


def mostrar_catalogo():
    print("--- Catálogo ---")
    for producto, precio in CATALOGO.items():
        print(f"{producto:<8}{precio:>7.2f}")


def registrar_venta():
    """Pide los productos de una venta, la guarda y devuelve el total."""
    lineas = []
    nombre = input("Producto (vacío para cerrar): ").strip().lower()
    while nombre != "":
        if nombre in CATALOGO:
            cantidad = pedir_entero("Cantidad: ")
            lineas.append((nombre, cantidad, CATALOGO[nombre] * cantidad))
        else:
            print(f"'{nombre}' no está en el catálogo")
        nombre = input("Producto (vacío para cerrar): ").strip().lower()

    if not lineas:
        print("Venta cancelada: no se agregó ningún producto")
        return 0

    subtotal = sum(importe for _, _, importe in lineas)
    porcentaje = calcular_descuento(subtotal)
    total = aplicar_descuento(subtotal, porcentaje)
    for producto, cantidad, importe in lineas:
        # El descuento se reparte en proporción al importe de cada línea
        guardar_venta(producto, cantidad, aplicar_descuento(importe, porcentaje))
    print(f"Subtotal: {subtotal:.2f}  Descuento: {porcentaje} %")
    print(f"Total a pagar: {total:.2f}")
    return total


def mostrar_reporte():
    filas = leer_ventas()
    unidades = ventas_por_producto(filas)
    print("--- Reporte ---")
    print(f"Líneas de venta registradas: {len(filas)}")
    print(f"Total vendido: {total_vendido(filas):.2f}")
    for producto, cantidad in sorted(unidades.items()):
        print(f"  {producto:<8}{cantidad:>5} u.")
    mas = producto_mas_vendido(unidades)
    if mas is not None:
        print(f"Producto más vendido: {mas}")


def main():
    while True:
        print("=== MiTienda v1.0 ===")
        print("1. Registrar venta")
        print("2. Ver catálogo")
        print("3. Reporte de ventas")
        print("4. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            registrar_venta()
        elif opcion == "2":
            mostrar_catalogo()
        elif opcion == "3":
            mostrar_reporte()
        elif opcion == "4":
            print("Hasta pronto")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
