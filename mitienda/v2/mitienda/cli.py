"""Interfaz de consola de MiTienda v2: solo conversa con el usuario."""

from datetime import datetime

from mitienda import __version__, almacen

CATALOGO_INICIAL = {
    "pan": (0.5, 200),
    "leche": (6.0, 30),
    "queso": (45.0, 8),
    "arroz": (9.5, 40),
}


def pedir_entero(mensaje: str, minimo: int = 1) -> int:
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Escribe un número entero, por ejemplo 3")
            continue
        if numero >= minimo:
            return numero
        print(f"Debe ser mayor o igual que {minimo}")


def cargar_catalogo_inicial(con) -> None:
    if not almacen.listar_productos(con):
        for nombre, (precio, stock) in CATALOGO_INICIAL.items():
            almacen.agregar_producto(con, nombre, precio, stock)


def opcion_vender(con) -> None:
    pedido: dict[str, int] = {}
    nombre = input("Producto (vacío para cerrar): ").strip().lower()
    while nombre:
        cantidad = pedir_entero("Cantidad: ")
        pedido[nombre] = pedido.get(nombre, 0) + cantidad
        nombre = input("Producto (vacío para cerrar): ").strip().lower()
    try:
        venta_id = almacen.registrar_venta(con, pedido)
    except almacen.ErrorDeVenta as error:
        print(f"No se registró la venta: {error}")
        return
    total = con.execute(
        "SELECT total FROM ventas WHERE id = ?", (venta_id,)
    ).fetchone()[0]
    print(f"Venta N.º {venta_id} registrada. Total a pagar: {total:.2f}")


def opcion_catalogo(con) -> None:
    print(f"{'Producto':<10}{'Precio':>8}{'Stock':>7}")
    for p in almacen.listar_productos(con):
        print(f"{p['nombre']:<10}{p['precio']:>8.2f}{p['stock']:>7}")


def opcion_reporte(con) -> None:
    hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"Total vendido hoy: {almacen.total_del_dia(con, hoy):.2f}")
    reponer = almacen.productos_para_reponer(con)
    if reponer:
        print("Reponer: " + ", ".join(f"{p['nombre']} ({p['stock']})" for p in reponer))


def opcion_anular(con) -> None:
    venta_id = pedir_entero("N.º de venta a anular: ")
    if almacen.anular_venta(con, venta_id):
        print(f"Venta {venta_id} anulada; el stock se devolvió")
    else:
        print("Esa venta no existe o ya estaba anulada")


def opcion_exportar(con) -> None:
    mes = datetime.now().strftime("%Y-%m")
    ruta = f"ventas_{mes}.csv"
    n = almacen.exportar_mes(con, mes, ruta)
    print(f"Se exportaron {n} líneas a {ruta}")


OPCIONES = {
    "1": ("Registrar venta", opcion_vender),
    "2": ("Ver catálogo y stock", opcion_catalogo),
    "3": ("Reporte del día", opcion_reporte),
    "4": ("Anular venta", opcion_anular),
    "5": ("Exportar ventas del mes", opcion_exportar),
}


def main(ruta_db: str = "mitienda.db") -> None:
    con = almacen.conectar(ruta_db)
    cargar_catalogo_inicial(con)
    while True:
        print(f"=== MiTienda v{__version__} ===")
        for clave, (texto, _) in OPCIONES.items():
            print(f"{clave}. {texto}")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "0":
            print("Hasta pronto")
            break
        if opcion in OPCIONES:
            OPCIONES[opcion][1](con)
        else:
            print("Opción no válida")
    con.close()


if __name__ == "__main__":
    main()
