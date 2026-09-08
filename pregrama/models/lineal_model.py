import sympy as sp

from sympy import (
    symbols,
    Function,
    Eq,
    exp,
    integrate,
    solve,
    dsolve
)

from models.helpers import parsear_expresion, sym_latex


def resolver_lineal(P_str, Q_str, variable, x0=None, y0=None):

    pasos = []

    x = symbols(variable)

    y = Function("y")

    C1 = symbols("C1")

    # ===========================
    # Convertir expresiones
    # ===========================

    P = parsear_expresion(
        P_str,
        simbolos={
            "x": x,
            "t": x
        }
    )

    Q = parsear_expresion(
        Q_str,
        simbolos={
            "x": x,
            "t": x
        }
    )

    # ===========================
    # Mostrar datos
    # ===========================

    pasos.append({

        "tipo": "info",

        "texto":
            f"Forma estándar: dy/d{variable} + "
            f"P({variable})y = Q({variable})"

    })

    pasos.append({

        "tipo": "resultado",

        "texto": f"P({variable})",

        "formula": sym_latex(P)

    })

    pasos.append({

        "tipo": "resultado",

        "texto": f"Q({variable})",

        "formula": sym_latex(Q)

    })

    # ===========================
    # Factor integrante
    # ===========================

    mu = exp(

        integrate(

            P,

            x

        )

    )

    pasos.append({

        "tipo": "titulo",

        "texto": "Factor Integrante"

    })

    pasos.append({

        "tipo": "formula",

        "formula":

            f"\\mu({variable}) = "

            f"e^{{\\int P d{variable}}}"

            f" = {sym_latex(mu)}"

    })

    # ===========================
    # Resolver EDO
    # ===========================

    ecuacion = Eq(

        y(x).diff(x) +

        P * y(x),

        Q

    )

    solucion = dsolve(

        ecuacion,

        y(x)

    )

    pasos.append({

        "tipo": "titulo",

        "texto": "Solución General"

    })

    pasos.append({

        "tipo": "formula",

        "formula": sym_latex(solucion)

    })

    # ===========================
    # Condición inicial
    # ===========================

    if (x0 is None) != (y0 is None):
        raise ValueError("Debes indicar ambos valores de la condición inicial o ninguno.")

    if x0 is not None and y0 is not None:

        pasos.append({

            "tipo": "titulo",

            "texto":

                f"Aplicando condición "

                f"y({x0}) = {y0}"

        })

        try:

            constante = solve(

                solucion.rhs.subs(

                    x,

                    float(x0)

                ) - float(y0),

                C1

            )

            if constante:

                solucion_particular = solucion.subs(

                    C1,

                    constante[0]

                )

                pasos.append({

                    "tipo": "resultado",

                    "texto": "Constante C₁",

                    "formula":

                        sym_latex(

                            constante[0]

                        )

                })

                pasos.append({

                    "tipo": "formula",

                    "formula":

                        sym_latex(

                            solucion_particular

                        )

                })

        except Exception:

            pasos.append({

                "tipo": "warn",

                "texto":

                    "No fue posible aplicar "

                    "la condición inicial."

            })

    return pasos