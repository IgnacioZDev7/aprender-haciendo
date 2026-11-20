from mitienda import cli


def simular_teclado(monkeypatch, respuestas):
    """Reemplaza input() por una función que devuelve las respuestas en orden."""
    entradas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda mensaje="": next(entradas))


def test_pedir_entero_insiste_hasta_dato_valido(monkeypatch, capsys):
    simular_teclado(monkeypatch, ["tres", "0", "3"])
    assert cli.pedir_entero("Cantidad: ") == 3
    salida = capsys.readouterr().out
    assert "Escribe un número entero" in salida
    assert "mayor o igual que 1" in salida


def test_sesion_completa(monkeypatch, capsys, tmp_path):
    simular_teclado(monkeypatch, ["1", "queso", "3", "pan", "10", "", "3", "0"])
    cli.main(str(tmp_path / "prueba.db"))
    salida = capsys.readouterr().out
    assert "Venta N.º 1 registrada. Total a pagar: 133.00" in salida
    assert "Reponer: queso (5)" in salida
