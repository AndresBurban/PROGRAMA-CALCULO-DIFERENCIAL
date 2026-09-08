import sympy as sp

from sympy import (
    symbols,
    diff,
    simplify,
    integrate,
    exp,
    Eq,
    Function,
    dsolve
)

from models.helpers import parsear_expresion, sym_latex
from models.exacta_model import resolver_exacta


def resolver_no_exacta(M_str, N_str):

    pasos = []

    x, y = symbols("x y")

    # ====================================
    # Conversión a expresiones SymPy
    # ====================================

    M = parsear_expresion(

        M_str,

        simbolos={

            "x": x,

            "y": y

        }

    )

    N = parsear_expresion(

        N_str,

        simbolos={

            "x": x,

            "y": y

        }

    )

    # ====================================
    # Derivadas parciales
    # ====================================

    dM_dy = diff(

        M,

        y

    )

    dN_dx = diff(

        N,

        x

    )

    diferencia = simplify(

        dM_dy - dN_dx

    )

    pasos.append({

        "tipo": "titulo",

        "texto": "Verificación Inicial"

    })

    pasos.append({

        "tipo": "resultado",

        "texto": "∂M/∂y − ∂N/∂x",

        "formula": sym_latex(diferencia)

    })

    # ====================================
    # ¿Ya es exacta?
    # ====================================

    if diferencia == 0:

        pasos.append({

            "tipo": "ok",

            "texto":

            "La ecuación ya es exacta."

        })

        pasos.extend(

            resolver_exacta(

                M_str,

                N_str

            )

        )

        return pasos

    # ====================================
    # Buscar μ(x)
    # ====================================

    pasos.append({

        "tipo": "titulo",

        "texto":

        "Buscando Factor Integrante μ(x)"

    })

    try:

        fx = simplify(

            diferencia / N

        )

        pasos.append({

            "tipo": "resultado",

            "texto":

            "(∂M/∂y−∂N/∂x)/N",

            "formula":

            sym_latex(fx)

        })

        if not fx.free_symbols - {x}:

            mu = exp(

                integrate(

                    fx,

                    x

                )

            )

            pasos.append({

                "tipo": "ok",

                "texto":

                "Factor integrante encontrado."

            })

            pasos.append({

                "tipo": "resultado",

                "texto": "μ(x)",

                "formula":

                sym_latex(mu)

            })

            pasos.extend(

                resolver_exacta(

                    str(

                        simplify(

                            mu * M

                        )

                    ),

                    str(

                        simplify(

                            mu * N

                        )

                    )

                )

            )

            return pasos

    except Exception:

        pass

    # ====================================
    # Buscar μ(y)
    # ====================================

    pasos.append({

        "tipo": "titulo",

        "texto":

        "Buscando Factor Integrante μ(y)"

    })

    try:

        fy = simplify(

            (

                dN_dx - dM_dy

            ) / M

        )

        pasos.append({

            "tipo": "resultado",

            "texto":

            "(∂N/∂x−∂M/∂y)/M",

            "formula":

            sym_latex(fy)

        })

        if not fy.free_symbols - {y}:

            mu = exp(

                integrate(

                    fy,

                    y

                )

            )

            pasos.append({

                "tipo": "ok",

                "texto":

                "Factor integrante encontrado."

            })

            pasos.append({

                "tipo": "resultado",

                "texto": "μ(y)",

                "formula":

                sym_latex(mu)

            })

            pasos.extend(

                resolver_exacta(

                    str(

                        simplify(

                            mu * M

                        )

                    ),

                    str(

                        simplify(

                            mu * N

                        )

                    )

                )

            )

            return pasos

    except Exception:

        pass

    # ====================================
    # Resolver mediante dsolve
    # ====================================

    pasos.append({

        "tipo": "warn",

        "texto":

        "No se encontró un factor integrante simple. Se utilizará SymPy."

    })

    yf = Function("y")

    ecuacion = Eq(

        M +

        N * yf(x).diff(x),

        0

    )

    solucion = dsolve(

        ecuacion,

        yf(x)

    )

    pasos.append({

        "tipo": "titulo",

        "texto":

        "Solución"

    })

    pasos.append({

        "tipo": "formula",

        "formula":

        sym_latex(solucion)

    })

    return pasos