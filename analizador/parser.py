from sympy import (
    Abs,
    E,
    Piecewise,
    acos,
    asin,
    atan,
    cos,
    exp,
    log,
    pi,
    sin,
    sqrt,
    symbols,
    sympify,
    tan,
)
from sympy.core.symbol import Symbol

from .errores import ErrorParser

x = symbols("x", real=True)

NOMBRES_PERMITIDOS = {
    "x": x,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "log": log,
    "sqrt": sqrt,
    "exp": exp,
    "abs": Abs,
    "Abs": Abs,
    "Piecewise": Piecewise,
    "E": E,
    "pi": pi,
}


def parsear_expresion(texto: str):
    if not isinstance(texto, str) or not texto.strip():
        raise ErrorParser("La función está vacía.")
    if "__" in texto or ";" in texto:
        raise ErrorParser("La expresión contiene símbolos no permitidos.")
    try:
        expr = sympify(
            texto,
            locals=NOMBRES_PERMITIDOS,
            convert_xor=True,
            evaluate=True,
            rational=True,
        )
    except Exception as e:
        raise ErrorParser(f"No se pudo interpretar la función: {e}")
    # verificar solo variable x
    simbolos = [s for s in expr.free_symbols if isinstance(s, Symbol)]
    if any(str(s) != "x" for s in simbolos):
        raise ErrorParser("Solo se permite la variable x.")
    return expr
