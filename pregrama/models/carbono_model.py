import sympy as sp

from sympy import (
    symbols,
    Eq,
    Function,
    dsolve,
    exp,
    log,
    N
)

from models.helpers import sym_latex


def resolver_carbono(
    vida_media,
    cantidad_inicial,
    cantidad_final
):

    # =====================================
    # Validaciones
    # =====================================

    if vida_media <= 0:
        raise ValueError(
            "La vida media debe ser mayor que cero."
        )

    if cantidad_inicial <= 0:
        raise ValueError(
            "La cantidad inicial debe ser mayor que cero."
        )

    if cantidad_final <= 0:
        raise ValueError(
            "La cantidad final debe ser mayor que cero."
        )

    if cantidad_final > cantidad_inicial:
        raise ValueError(
            "La cantidad final no puede superar "
            "la cantidad inicial."
        )

    # =====================================
    # Variables simbólicas
    # =====================================

    pasos = []

    t = symbols(
        "t",
        positive=True
    )

    C = Function("C")

    k = symbols(
        "k",
        positive=True
    )

    # =====================================
    # DATOS
    # =====================================

    pasos.append({
        "tipo": "titulo",
        "texto": "Datos del problema"
    })

    pasos.append({
        "tipo": "resultado",
        "texto": "Vida media",
        "formula": str(vida_media) + " años"
    })

    pasos.append({
        "tipo": "resultado",
        "texto": "Cantidad inicial",
        "formula": str(cantidad_inicial)
    })

    pasos.append({
        "tipo": "resultado",
        "texto": "Cantidad final",
        "formula": str(cantidad_final)
    })

    # =====================================
    # MODELO DIFERENCIAL
    # =====================================

    ecuacion = Eq(
        C(t).diff(t),
        -k * C(t)
    )

    pasos.append({
        "tipo": "titulo",
        "texto": "Modelo diferencial"
    })

    pasos.append({
        "tipo": "formula",
        "formula": sym_latex(ecuacion)
    })

    # =====================================
    # SOLUCIÓN GENERAL
    # =====================================

    solucion = dsolve(
        ecuacion,
        C(t)
    )

    pasos.append({
        "tipo": "titulo",
        "texto": "Solución general"
    })

    pasos.append({
        "tipo": "formula",
        "formula": sym_latex(solucion)
    })

    # =====================================
    # CONSTANTE DE DECAIMIENTO
    # =====================================

    constante = log(2) / vida_media

    pasos.append({
        "tipo": "titulo",
        "texto": "Constante de decaimiento"
    })

    pasos.append({
        "tipo": "formula",
        "formula": (
            r"k = \frac{\ln(2)}{T_{1/2}}"
        )
    })

    pasos.append({
        "tipo": "formula",
        "formula": (
            r"k = " +
            sym_latex(constante)
        )
    })

    pasos.append({
        "tipo": "resultado",
        "texto": "Valor aproximado de k",
        "formula": (
            str(round(
                float(N(constante)),
                10
            ))
        )
    })

    # =====================================
    # MODELO PARTICULAR
    # =====================================

    modelo = (
        cantidad_inicial *
        exp(-constante * t)
    )

    pasos.append({
        "tipo": "titulo",
        "texto": "Modelo particular"
    })

    pasos.append({
        "tipo": "formula",
        "formula": (
            r"C(t) = " +
            sym_latex(modelo)
        )
    })

    # =====================================
    # DESPEJE DEL TIEMPO
    # =====================================

    pasos.append({
        "tipo": "titulo",
        "texto": "Cálculo del tiempo transcurrido"
    })

    pasos.append({
        "tipo": "formula",
        "formula": (
            r"C_f = C_0 e^{-kt}"
        )
    })

    pasos.append({
        "tipo": "formula",
        "formula": (
            r"t = \frac{\ln(C_0/C_f)}{k}"
        )
    })

    # =====================================
    # CÁLCULO DEL TIEMPO
    # =====================================

    tiempo = (
        log(
            cantidad_inicial /
            cantidad_final
        )
        /
        constante
    )

    pasos.append({
        "tipo": "formula",
        "formula": sym_latex(tiempo)
    })

    tiempo_numerico = round(
        float(N(tiempo)),
        2
    )

    pasos.append({
        "tipo": "resultado",
        "texto": "Edad aproximada de la muestra",
        "formula": (
            str(tiempo_numerico)
            + " años"
        )
    })

    return pasos