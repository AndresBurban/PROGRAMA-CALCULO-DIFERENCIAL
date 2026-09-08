import sympy as sp

from sympy import (
    symbols,
    integrate,
    diff,
    simplify,
    Eq
)

from models.helpers import parsear_expresion, sym_latex


def resolver_exacta(M_str, N_str, variable="x"):

    pasos = []

    x, y = symbols("x y")

    # ==========================
    # Convertir a SymPy
    # ==========================

    M = parsear_expresion(M_str, {"x": x, "y": y})

    N = parsear_expresion(N_str, {"x": x, "y": y})

    pasos.append({

        "tipo": "titulo",

        "texto": "Verificación de Exactitud"

    })

    pasos.append({

        "tipo": "resultado",

        "texto": "M(x,y)",

        "formula": sym_latex(M)

    })

    pasos.append({

        "tipo": "resultado",

        "texto": "N(x,y)",

        "formula": sym_latex(N)

    })

    # ==========================
    # Derivadas parciales
    # ==========================

    dMdy = diff(M, y)

    dNdx = diff(N, x)

    pasos.append({

        "tipo": "formula",

        "formula":
        f"\\frac{{\\partial M}}{{\\partial y}}={sym_latex(dMdy)}"

    })

    pasos.append({

        "tipo": "formula",

        "formula":
        f"\\frac{{\\partial N}}{{\\partial x}}={sym_latex(dNdx)}"

    })

    # ==========================
    # ¿Es exacta?
    # ==========================

    if simplify(dMdy - dNdx) != 0:

        pasos.append({

            "tipo": "warn",

            "texto":
            "La ecuación NO es exacta."

        })

        return pasos

    pasos.append({

        "tipo": "ok",

        "texto":
        "La ecuación es exacta."

    })

    # ==========================
    # Integrar M
    # ==========================

    F = integrate(M, x)

    pasos.append({

        "tipo": "titulo",

        "texto":
        "Integración respecto a x"

    })

    pasos.append({

        "tipo": "formula",

        "formula":
        sym_latex(F)

    })

    # ==========================
    # Obtener g(y)
    # ==========================

    gprima = simplify(

        N - diff(F, y)

    )

    pasos.append({

        "tipo": "titulo",

        "texto":
        "Cálculo de g(y)"

    })

    pasos.append({

        "tipo": "formula",

        "formula":
        sym_latex(gprima)

    })

    g = integrate(

        gprima,

        y

    )

    pasos.append({

        "tipo": "formula",

        "formula":
        sym_latex(g)

    })

    # ==========================
    # Solución final
    # ==========================

    solucion = simplify(

        F + g

    )

    pasos.append({

        "tipo": "titulo",

        "texto":
        "Solución Implícita"

    })

    pasos.append({

        "tipo": "formula",

        "formula":
        sym_latex(

            Eq(solucion, symbols("C"))

        )

    })

    return pasos