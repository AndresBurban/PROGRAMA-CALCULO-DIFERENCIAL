from sympy import Eq, Function, integrate, simplify, symbols

from models.helpers import parsear_expresion, sym_latex


def resolver_separable(f_str, g_str, x0=None, y0=None):
    pasos = []
    x, y = symbols("x y")

    f = parsear_expresion(f_str, {"x": x})
    g = parsear_expresion(g_str, {"y": y})

    if simplify(g) == 0:
        raise ValueError("g(y) no puede ser identicamente cero.")

    pasos.append({
        "tipo": "info",
        "texto": "Forma estandar: dy/dx = f(x) * g(y)"
    })
    pasos.append({"tipo": "resultado", "texto": "f(x)", "formula": sym_latex(f)})
    pasos.append({"tipo": "resultado", "texto": "g(y)", "formula": sym_latex(g)})

    if (x0 is None) != (y0 is None):
        raise ValueError("Debes indicar ambos valores de la condicion inicial o ninguno.")

    x0_value = None
    y0_value = None
    if x0 is not None and y0 is not None:
        try:
            x0_value = float(x0)
            y0_value = float(y0)
        except (TypeError, ValueError) as error:
            raise ValueError("x0 y y0 deben ser valores numericos.") from error

        if simplify(g.subs(y, y0_value)).is_zero:
            pasos.append({
                "tipo": "titulo",
                "texto": f"Aplicando condicion y({x0}) = {y0}"
            })
            pasos.append({
                "tipo": "formula",
                "formula": f"y = {sym_latex(y0_value)}"
            })
            pasos.append({
                "tipo": "info",
                "texto": "La condicion inicial produce una solucion constante."
            })
            return pasos

    inversa_g = simplify(1 / g)
    pasos.append({
        "tipo": "titulo",
        "texto": "Separacion de variables"
    })
    pasos.append({
        "tipo": "formula",
        "formula": (
            f"\\frac{{1}}{{{sym_latex(g)}}}dy = "
            f"{sym_latex(f)}dx"
        )
    })

    integral_y = integrate(inversa_g, y)
    integral_x = integrate(f, x)

    pasos.append({
        "tipo": "titulo",
        "texto": "Integracion de ambos lados"
    })
    pasos.append({
        "tipo": "formula",
        "formula": f"{sym_latex(integral_y)} = {sym_latex(integral_x)} + C"
    })

    if x0 is not None and y0 is not None:
        constante = simplify(
            integral_y.subs(y, y0_value) - integral_x.subs(x, x0_value)
        )

        pasos.append({
            "tipo": "titulo",
            "texto": f"Aplicando condicion y({x0}) = {y0}"
        })
        pasos.append({
            "tipo": "formula",
            "formula": (
                f"{sym_latex(integral_y)} - {sym_latex(constante)} "
                f"= {sym_latex(integral_x - integral_x.subs(x, x0_value))}"
            )
        })
    else:
        pasos.append({
            "tipo": "titulo",
            "texto": "Solucion general"
        })
        pasos.append({
            "tipo": "formula",
            "formula": sym_latex(Eq(integral_y, integral_x + symbols("C")))
        })

    pasos.append({
        "tipo": "info",
        "texto": "Las soluciones constantes que cumplen g(y) = 0 deben analizarse por separado."
    })

    return pasos