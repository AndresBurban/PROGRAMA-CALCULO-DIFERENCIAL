import re

import sympy as sp
from sympy import latex


_NOMBRES_MATEMATICOS = {
    "x", "y", "t", "pi", "E", "sin", "cos", "tan", "exp", "log", "sqrt"
}


def parsear_expresion(expresion, simbolos=None):
    """Convierte una expresión usando únicamente nombres matemáticos permitidos."""

    if not isinstance(expresion, str) or not expresion.strip():
        raise ValueError("La expresión matemática no puede estar vacía.")

    nombres = re.findall(r"[A-Za-z]+", expresion)
    if not re.fullmatch(r"[0-9A-Za-z+*/^().,\s-]+", expresion) or any(
        nombre not in _NOMBRES_MATEMATICOS for nombre in nombres
    ):
        raise ValueError("La expresión contiene símbolos o funciones no permitidos.")

    locales = {nombre: getattr(sp, nombre) for nombre in _NOMBRES_MATEMATICOS if hasattr(sp, nombre)}
    if simbolos:
        locales.update(simbolos)
    return sp.sympify(expresion, locals=locales)


def sym_latex(expr):
    """
    Convierte una expresión de SymPy a formato LaTeX.
    """

    try:
        return latex(expr)
    except Exception:
        return str(expr)


def pasos_to_html(pasos):
    """
    Convierte la lista de pasos en HTML para mostrar
    el procedimiento en la interfaz.
    """

    html = ""

    for paso in pasos:

        tipo = paso.get("tipo", "info")
        texto = paso.get("texto", "")
        formula = paso.get("formula", "")

        if tipo == "titulo":

            html += f"""
            <h6 class="mt-3 text-accent fw-bold">
                ▶ {texto}
            </h6>
            """

        elif tipo == "resultado":

            html += f"""
            <div class="result-box my-2">

                <span class="label">
                    {texto}:
                </span>

                <span class="formula">
                    \\({formula}\\)
                </span>

            </div>
            """

        elif tipo == "formula":

            html += f"""
            <div class="formula-display my-2">
                \\[
                    {formula}
                \\]
            </div>
            """

        elif tipo == "info":

            html += f"""
            <p class="mb-1 text-muted small">
                {texto}
            </p>
            """

        elif tipo == "ok":

            html += f"""
            <div class="alert alert-success py-1 px-3 small">
                {texto}
            </div>
            """

        elif tipo == "warn":

            html += f"""
            <div class="alert alert-warning py-1 px-3 small">
                {texto}
            </div>
            """

    return html