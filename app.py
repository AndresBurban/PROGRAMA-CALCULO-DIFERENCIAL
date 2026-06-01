"""
Servidor Flask — Taller de Ecuaciones Diferenciales
Backend con SymPy + NumPy
"""

from flask import Flask, request, jsonify, render_template_string
import sympy as sp
from sympy import (
    symbols, Function, dsolve, Eq, exp, ln, solve, oo,
    simplify, diff, integrate, latex, pretty, limit
)
import numpy as np
import warnings, traceback

warnings.filterwarnings("ignore")

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────

def sym_latex(expr):
    try:
        return latex(expr)
    except:
        return str(expr)

def pasos_to_html(pasos):
    html = ""
    for p in pasos:
        tipo = p.get("tipo", "paso")
        texto = p.get("texto", "")
        formula = p.get("formula", "")
        if tipo == "titulo":
            html += f'<h6 class="mt-3 text-accent fw-bold">▶ {texto}</h6>'
        elif tipo == "resultado":
            html += f'<div class="result-box my-2"><span class="label">{texto}:</span> <span class="formula">\\({formula}\\)</span></div>'
        elif tipo == "info":
            html += f'<p class="mb-1 text-muted small">{texto}</p>'
        elif tipo == "formula":
            html += f'<div class="formula-display my-2">\\[{formula}\\]</div>'
        elif tipo == "ok":
            html += f'<div class="alert alert-success py-1 px-3 small">{texto}</div>'
        elif tipo == "warn":
            html += f'<div class="alert alert-warning py-1 px-3 small">{texto}</div>'
    return html

# ─────────────────────────────────────────────────────────────────
# SOLVERS
# ─────────────────────────────────────────────────────────────────

def resolver_lineal(P_str, Q_str, var, x0=None, y0=None):
    pasos = []
    x = symbols(var)
    y = Function('y')
    C1 = symbols('C1')

    P = sp.sympify(P_str, locals={'x': x, 't': x})
    Q = sp.sympify(Q_str, locals={'x': x, 't': x})

    pasos.append({"tipo": "info", "texto": f"Forma estándar: dy/d{var} + P({var})·y = Q({var})"})
    pasos.append({"tipo": "resultado", "texto": f"P({var})", "formula": sym_latex(P)})
    pasos.append({"tipo": "resultado", "texto": f"Q({var})", "formula": sym_latex(Q)})

    # Factor integrante
    mu = exp(integrate(P, x))
    pasos.append({"tipo": "titulo", "texto": "Factor integrante μ"})
    pasos.append({"tipo": "formula", "formula": f"\\mu({var}) = e^{{\\int P\\,d{var}}} = {sym_latex(mu)}"})

    # Solución general
    ode = Eq(y(x).diff(x) + P * y(x), Q)
    sol = dsolve(ode, y(x))
    pasos.append({"tipo": "titulo", "texto": "Solución general"})
    pasos.append({"tipo": "formula", "formula": sym_latex(sol)})

    # Condición inicial
    if x0 is not None and y0 is not None:
        pasos.append({"tipo": "titulo", "texto": f"Condición inicial y({x0}) = {y0}"})
        try:
            c_val = solve(sol.rhs.subs(x, float(x0)) - float(y0), C1)
            if c_val:
                sol_p = sol.subs(C1, c_val[0])
                pasos.append({"tipo": "resultado", "texto": "C₁", "formula": sym_latex(c_val[0])})
                pasos.append({"tipo": "formula", "formula": sym_latex(sol_p)})
        except:
            pasos.append({"tipo": "warn", "texto": "No se pudo aplicar la condición inicial automáticamente."})

    return pasos

def resolver_exacta(M_str, N_str):
    pasos = []
    x, y = symbols('x y')

    M = sp.sympify(M_str, locals={'x': x, 'y': y})
    N = sp.sympify(N_str, locals={'x': x, 'y': y})

    pasos.append({"tipo": "resultado", "texto": "M(x,y)", "formula": sym_latex(M)})
    pasos.append({"tipo": "resultado", "texto": "N(x,y)", "formula": sym_latex(N)})

    dM_dy = diff(M, y)
    dN_dx = diff(N, x)

    pasos.append({"tipo": "titulo", "texto": "Verificación de exactitud"})
    pasos.append({"tipo": "resultado", "texto": "∂M/∂y", "formula": sym_latex(dM_dy)})
    pasos.append({"tipo": "resultado", "texto": "∂N/∂x", "formula": sym_latex(dN_dx)})

    exacta = simplify(dM_dy - dN_dx) == 0

    if exacta:
        pasos.append({"tipo": "ok", "texto": "✔ La ecuación ES EXACTA (∂M/∂y = ∂N/∂x)"})
        F = integrate(M, x)
        pasos.append({"tipo": "titulo", "texto": "Construyendo F(x,y)"})
        pasos.append({"tipo": "formula", "formula": f"F = \\int M\\,dx = {sym_latex(F)} + g(y)"})

        dF_dy = diff(F, y)
        g_prima = simplify(N - dF_dy)
        g_y = integrate(g_prima, y)
        F_total = simplify(F + g_y)

        pasos.append({"tipo": "resultado", "texto": "g'(y)", "formula": sym_latex(g_prima)})
        pasos.append({"tipo": "resultado", "texto": "g(y)", "formula": sym_latex(g_y)})
        pasos.append({"tipo": "titulo", "texto": "Solución implícita"})
        pasos.append({"tipo": "formula", "formula": f"{sym_latex(F_total)} = C"})
    else:
        pasos.append({"tipo": "warn", "texto": "✘ La ecuación NO es exacta. Buscando factor integrante..."})
        ratio = simplify((dM_dy - dN_dx) / N)
        if not ratio.free_symbols - {x}:
            mu = exp(integrate(ratio, x))
            pasos.append({"tipo": "resultado", "texto": "μ(x)", "formula": sym_latex(mu)})
            pasos += resolver_exacta(str(simplify(mu*M)), str(simplify(mu*N)))
        else:
            ratio2 = simplify((dN_dx - dM_dy) / M)
            if not ratio2.free_symbols - {y}:
                mu = exp(integrate(ratio2, y))
                pasos.append({"tipo": "resultado", "texto": "μ(y)", "formula": sym_latex(mu)})
                pasos += resolver_exacta(str(simplify(mu*M)), str(simplify(mu*N)))
            else:
                pasos.append({"tipo": "warn", "texto": "No se encontró factor integrante simple."})
    return pasos

def resolver_no_exacta(M_str, N_str):
    pasos = []
    x, y = symbols('x y')
    M = sp.sympify(M_str, locals={'x': x, 'y': y})
    N = sp.sympify(N_str, locals={'x': x, 'y': y})

    dM_dy = diff(M, y)
    dN_dx = diff(N, x)
    diff_val = simplify(dM_dy - dN_dx)

    pasos.append({"tipo": "info", "texto": "Verificando si es exacta primero..."})
    pasos.append({"tipo": "resultado", "texto": "∂M/∂y − ∂N/∂x", "formula": sym_latex(diff_val)})

    if diff_val == 0:
        pasos.append({"tipo": "ok", "texto": "¡Ya es exacta! Resolviendo directamente."})
        pasos += resolver_exacta(M_str, N_str)
        return pasos

    pasos.append({"tipo": "titulo", "texto": "Buscando factor integrante μ(x)"})
    try:
        fx = simplify(diff_val / N)
        pasos.append({"tipo": "resultado", "texto": "(∂M/∂y − ∂N/∂x) / N", "formula": sym_latex(fx)})
        if not fx.free_symbols - {x}:
            mu = exp(integrate(fx, x))
            pasos.append({"tipo": "ok", "texto": f"✔ Factor integrante μ(x) encontrado"})
            pasos.append({"tipo": "resultado", "texto": "μ(x)", "formula": sym_latex(mu)})
            pasos += resolver_exacta(str(simplify(mu*M)), str(simplify(mu*N)))
            return pasos
    except:
        pass

    pasos.append({"tipo": "titulo", "texto": "Buscando factor integrante μ(y)"})
    try:
        fy = simplify((dN_dx - dM_dy) / M)
        pasos.append({"tipo": "resultado", "texto": "(∂N/∂x − ∂M/∂y) / M", "formula": sym_latex(fy)})
        if not fy.free_symbols - {y}:
            mu = exp(integrate(fy, y))
            pasos.append({"tipo": "ok", "texto": f"✔ Factor integrante μ(y) encontrado"})
            pasos.append({"tipo": "resultado", "texto": "μ(y)", "formula": sym_latex(mu)})
            pasos += resolver_exacta(str(simplify(mu*M)), str(simplify(mu*N)))
            return pasos
    except:
        pass

    pasos.append({"tipo": "warn", "texto": "No se halló factor integrante simple. Usando dsolve general."})
    yf = Function('y')
    ode = Eq(M + N * yf(x).diff(x), 0)
    sol = dsolve(ode, yf(x))
    pasos.append({"tipo": "formula", "formula": sym_latex(sol)})
    return pasos

def resolver_carbono14(A0, At, t_med, vida_media=5730):
    pasos = []
    t = symbols('t', positive=True)
    k_val = -np.log(2) / vida_media
    k_sym = -ln(2) / vida_media

    pasos.append({"tipo": "info", "texto": f"Modelo: dA/dt = kA  →  A(t) = A₀·e^(kt)"})
    pasos.append({"tipo": "resultado", "texto": "Vida media C-14", "formula": f"{vida_media}\\text{{ años}}"})
    pasos.append({"tipo": "resultado", "texto": "k", "formula": f"\\frac{{-\\ln 2}}{{{vida_media}}} \\approx {k_val:.8f}"})

    pasos.append({"tipo": "titulo", "texto": "Solución general"})
    pasos.append({"tipo": "formula", "formula": f"A(t) = A_0 \\cdot e^{{kt}}"})

    if A0 and At and t_med:
        pasos.append({"tipo": "titulo", "texto": "Datación de la muestra"})
        prop = At / A0
        edad = np.log(prop) / k_val
        pasos.append({"tipo": "resultado", "texto": "A₀", "formula": f"{A0}\\text{{ g}}"})
        pasos.append({"tipo": "resultado", "texto": "A(t)", "formula": f"{At}\\text{{ g}}"})
        pasos.append({"tipo": "resultado", "texto": "Proporción", "formula": f"{prop:.4f}"})
        pasos.append({"tipo": "formula", "formula": f"t = \\frac{{\\ln({prop:.4f})}}{{k}} \\approx {edad:.1f}\\text{{ años}}"})
        pasos.append({"tipo": "ok", "texto": f"✔ Edad estimada: {edad:.0f} años"})

    return pasos

# ─────────────────────────────────────────────────────────────────
# EJERCICIOS DEL TALLER
# ─────────────────────────────────────────────────────────────────

EJERCICIOS = {
    "1": {
        "titulo": "Crecimiento Poblacional",
        "enunciado": "La población de una comunidad crece proporcionalmente al número de habitantes presentes. Inicialmente hay 500 habitantes y después de 4 años hay 900. dP/dt = kP",
        "items": ["Plantee la solución general", "Determine la función P(t)", "Calcule la población al cabo de 8 años"]
    },
    "2": {
        "titulo": "Decaimiento Radiactivo",
        "enunciado": "Una sustancia radiactiva se desintegra a una tasa proporcional a la cantidad presente. Inicialmente hay 100 g y después de 5 horas quedan 60 g.",
        "items": ["Modele el problema", "Encuentre la función A(t)", "Determine la vida media"]
    },
    "3": {
        "titulo": "Enfriamiento — Ley de Newton",
        "enunciado": "Un objeto se enfría en un ambiente de 20°C. Inicialmente está a 80°C y a los 10 minutos está a 50°C.",
        "items": ["Formule la ecuación diferencial", "Halle la función T(t)", "Determine la temperatura en 20 minutos"]
    },
    "4": {
        "titulo": "Mezclas",
        "enunciado": "Un tanque contiene 100 L de agua con 10 kg de sal. Entra agua salada con 0.5 kg/L a razón de 5 L/min y sale a la misma razón.",
        "items": ["Formule la ecuación diferencial", "Encuentre la función A(t)", "Determine el límite cuando t → ∞"]
    },
    "5": {
        "titulo": "Interés Compuesto Continuo",
        "enunciado": "Una inversión crece proporcionalmente al capital presente. Inicialmente se invierten $2000 a una tasa del 6% anual.",
        "items": ["Modele el crecimiento", "Encuentre S(t)", "Calcule el monto en 5 años"]
    },
    "6": {
        "titulo": "Absorción de Medicamento",
        "enunciado": "La concentración de un medicamento disminuye a una tasa proporcional a su concentración. Inicialmente hay 80 mg y después de 4 horas quedan 50 mg.",
        "items": ["Plantee la ecuación diferencial", "Encuentre la función de concentración", "¿Cuándo quedarán 20 mg?"]
    },
    "7": {
        "titulo": "Crecimiento con Entrada Constante",
        "enunciado": "Una población crece proporcionalmente a su tamaño, pero además recibe 50 individuos por año.",
        "items": ["Modele la situación", "Encuentre la solución general", "Determine la solución particular si P(0)=100"]
    },
    "8": {
        "titulo": "Descarga de Capacitor RC",
        "enunciado": "En un circuito RC, la carga en el capacitor disminuye proporcionalmente a la carga presente. dq/dt = -1/(RC)·q. Si inicialmente q(0) = 10 coulombs.",
        "items": ["Resuelva la ecuación diferencial", "Determine q(t)", "Encuentre el tiempo cuando la carga es 2 coulombs"]
    },
    "9": {
        "titulo": "Caída con Resistencia del Aire",
        "enunciado": "La velocidad de un objeto satisface: dv/dt = g − kv",
        "items": ["Identifique el tipo de ecuación diferencial", "Encuentre la solución general", "Determine la velocidad límite"]
    }
}

def resolver_ejercicio(num):
    pasos = []
    t = symbols('t', positive=True)
    k = symbols('k', real=True)
    C1 = symbols('C1')

    if num == "1":
        pasos.append({"tipo": "info", "texto": "dP/dt = kP,  P(0) = 500,  P(4) = 900"})
        pasos.append({"tipo": "titulo", "texto": "a) Solución general"})
        pasos.append({"tipo": "formula", "formula": "P(t) = C \\cdot e^{kt}"})
        pasos.append({"tipo": "titulo", "texto": "b) Determinando k con las condiciones iniciales"})
        C_val = 500
        k_eq = Eq(C_val * exp(4*k), 900)
        k_val = solve(k_eq, k)[0]
        k_num = float(k_val)
        pasos.append({"tipo": "formula", "formula": f"P(0)=500 \\Rightarrow C=500"})
        pasos.append({"tipo": "formula", "formula": f"P(4)=900 \\Rightarrow 500e^{{4k}}=900 \\Rightarrow k = \\frac{{\\ln(9/5)}}{{4}} \\approx {k_num:.6f}"})
        P_t = C_val * exp(k_val * t)
        pasos.append({"tipo": "resultado", "texto": "P(t)", "formula": f"500 \\cdot e^{{{sym_latex(k_val)}\\, t}}"})
        pasos.append({"tipo": "titulo", "texto": "c) Población en t = 8 años"})
        P8 = float(P_t.subs(t, 8))
        pasos.append({"tipo": "formula", "formula": f"P(8) = 500 \\cdot e^{{8 \\cdot {k_num:.6f}}} \\approx {P8:.0f}\\text{{ habitantes}}"})
        pasos.append({"tipo": "ok", "texto": f"✔ P(8) ≈ {round(P8)} habitantes"})

    elif num == "2":
        pasos.append({"tipo": "info", "texto": "dA/dt = kA,  A(0) = 100g,  A(5h) = 60g"})
        pasos.append({"tipo": "titulo", "texto": "a) Modelo"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dA}{dt} = kA \\quad (k < 0\\text{ decaimiento})"})
        pasos.append({"tipo": "titulo", "texto": "b) Función A(t)"})
        k_eq = Eq(100 * exp(5*k), 60)
        k_val = solve(k_eq, k)[0]
        k_num = float(k_val)
        pasos.append({"tipo": "formula", "formula": f"A(0)=100 \\Rightarrow A(t) = 100e^{{kt}}"})
        pasos.append({"tipo": "formula", "formula": f"A(5)=60 \\Rightarrow k = \\frac{{\\ln(3/5)}}{{5}} \\approx {k_num:.6f}"})
        pasos.append({"tipo": "resultado", "texto": "A(t)", "formula": f"100 \\cdot e^{{{k_num:.6f}\\,t}}"})
        pasos.append({"tipo": "titulo", "texto": "c) Vida media"})
        t_med = float(-np.log(2) / k_num)
        pasos.append({"tipo": "formula", "formula": f"t_{{1/2}} = \\frac{{-\\ln 2}}{{k}} \\approx {t_med:.2f}\\text{{ horas}}"})
        pasos.append({"tipo": "ok", "texto": f"✔ Vida media ≈ {t_med:.2f} horas"})

    elif num == "3":
        pasos.append({"tipo": "info", "texto": "T_amb = 20°C,  T(0) = 80°C,  T(10) = 50°C"})
        pasos.append({"tipo": "titulo", "texto": "a) Ecuación diferencial"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dT}{dt} = k(T - 20)"})
        pasos.append({"tipo": "titulo", "texto": "b) Función T(t)"})
        k_eq = Eq(20 + 60 * exp(10*k), 50)
        k_val = solve(k_eq, k)[0]
        k_num = float(k_val)
        pasos.append({"tipo": "formula", "formula": f"T(t) = 20 + 60\\,e^{{kt}},\\quad T(0)=80 \\Rightarrow C=60"})
        pasos.append({"tipo": "formula", "formula": f"T(10)=50 \\Rightarrow k = \\frac{{\\ln(1/2)}}{{10}} \\approx {k_num:.6f}"})
        pasos.append({"tipo": "resultado", "texto": "T(t)", "formula": f"20 + 60\\,e^{{{k_num:.6f}\\,t}} \\;°C"})
        pasos.append({"tipo": "titulo", "texto": "c) Temperatura en t = 20 min"})
        T20 = 20 + 60 * np.exp(k_num * 20)
        pasos.append({"tipo": "formula", "formula": f"T(20) = 20 + 60\\,e^{{20 \\cdot {k_num:.6f}}} = {T20:.2f}\\,°C"})
        pasos.append({"tipo": "ok", "texto": f"✔ T(20) = {T20:.2f} °C"})

    elif num == "4":
        pasos.append({"tipo": "info", "texto": "Tanque 100L, 10 kg sal, entrada 0.5 kg/L × 5 L/min"})
        pasos.append({"tipo": "titulo", "texto": "a) Ecuación diferencial"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dA}{dt} = 2.5 - \\frac{A}{20}"})
        pasos.append({"tipo": "info", "texto": "Ecuación lineal: dA/dt + (1/20)A = 2.5"})
        pasos.append({"tipo": "titulo", "texto": "b) Función A(t)"})
        A = Function('A')
        ode = Eq(A(t).diff(t) + A(t)/20, sp.Rational(5,2))
        sol = dsolve(ode, A(t))
        c_val = solve(sol.rhs.subs(t, 0) - 10, C1)[0]
        A_t = sol.rhs.subs(C1, c_val)
        pasos.append({"tipo": "formula", "formula": f"A(t) = {sym_latex(A_t)}"})
        pasos.append({"tipo": "titulo", "texto": "c) Límite cuando t → ∞"})
        lim = float(limit(A_t, t, oo))
        pasos.append({"tipo": "formula", "formula": f"\\lim_{{t \\to \\infty}} A(t) = {lim:.0f}\\text{{ kg}}"})
        pasos.append({"tipo": "ok", "texto": f"✔ Estado estacionario = {lim:.0f} kg (= 0.5 × 100)"})

    elif num == "5":
        pasos.append({"tipo": "info", "texto": "S(0) = $2000,  r = 6% anual"})
        pasos.append({"tipo": "titulo", "texto": "a) Modelo"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dS}{dt} = 0.06\\,S"})
        pasos.append({"tipo": "titulo", "texto": "b) Función S(t)"})
        pasos.append({"tipo": "formula", "formula": "S(t) = 2000\\,e^{0.06\\,t}"})
        pasos.append({"tipo": "titulo", "texto": "c) Monto en t = 5 años"})
        S5 = 2000 * np.exp(0.06 * 5)
        pasos.append({"tipo": "formula", "formula": f"S(5) = 2000\\,e^{{0.30}} \\approx \\${S5:.2f}"})
        pasos.append({"tipo": "ok", "texto": f"✔ S(5) ≈ ${S5:.2f}"})

    elif num == "6":
        pasos.append({"tipo": "info", "texto": "C(0) = 80mg,  C(4h) = 50mg,  ¿cuándo C = 20mg?"})
        pasos.append({"tipo": "titulo", "texto": "a) Ecuación diferencial"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dC}{dt} = kC \\quad (k < 0)"})
        pasos.append({"tipo": "titulo", "texto": "b) Función C(t)"})
        k_eq = Eq(80 * exp(4*k), 50)
        k_val = solve(k_eq, k)[0]
        k_num = float(k_val)
        pasos.append({"tipo": "formula", "formula": f"C(t) = 80\\,e^{{{k_num:.6f}\\,t}}"})
        pasos.append({"tipo": "titulo", "texto": "c) ¿Cuándo C = 20 mg?"})
        t_20 = float(np.log(20/80) / k_num)
        pasos.append({"tipo": "formula", "formula": f"20 = 80\\,e^{{kt}} \\Rightarrow t = \\frac{{\\ln(1/4)}}{{k}} \\approx {t_20:.2f}\\text{{ h}}"})
        pasos.append({"tipo": "ok", "texto": f"✔ C = 20 mg en t ≈ {t_20:.2f} horas"})

    elif num == "7":
        pasos.append({"tipo": "info", "texto": "dP/dt = kP + 50,  P(0) = 100"})
        pasos.append({"tipo": "titulo", "texto": "a) Modelo"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dP}{dt} = kP + 50"})
        pasos.append({"tipo": "titulo", "texto": "b) Solución general"})
        P = Function('P')
        ode = Eq(P(t).diff(t) - k * P(t), 50)
        sol = dsolve(ode, P(t))
        pasos.append({"tipo": "formula", "formula": sym_latex(sol)})
        pasos.append({"tipo": "titulo", "texto": "c) Con P(0) = 100"})
        c_vals = solve(sol.rhs.subs(t, 0) - 100, C1)
        if c_vals:
            P_part = sol.rhs.subs(C1, c_vals[0])
            pasos.append({"tipo": "resultado", "texto": "C₁", "formula": sym_latex(c_vals[0])})
            pasos.append({"tipo": "formula", "formula": f"P(t) = {sym_latex(P_part)}"})

    elif num == "8":
        pasos.append({"tipo": "info", "texto": "dq/dt = -q/(RC),  q(0) = 10 C"})
        pasos.append({"tipo": "titulo", "texto": "a) Solución de la EDO"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dq}{q} = -\\frac{dt}{RC} \\Rightarrow q(t) = q_0\\,e^{-t/RC}"})
        pasos.append({"tipo": "titulo", "texto": "b) q(t) con q(0) = 10"})
        pasos.append({"tipo": "formula", "formula": "q(t) = 10\\,e^{-t/RC}"})
        pasos.append({"tipo": "titulo", "texto": "c) ¿Cuándo q = 2 C?  (ejemplo RC = 1 s)"})
        t_2 = float(-1 * np.log(2/10))
        pasos.append({"tipo": "formula", "formula": f"2 = 10\\,e^{{-t}} \\Rightarrow t = \\ln(5) \\approx {t_2:.4f}\\text{{ s}}"})
        pasos.append({"tipo": "ok", "texto": f"✔ t = RC·ln(5) ≈ {t_2:.4f} s (para RC=1)"})

    elif num == "9":
        pasos.append({"tipo": "info", "texto": "dv/dt = g − kv"})
        pasos.append({"tipo": "titulo", "texto": "a) Tipo de ecuación"})
        pasos.append({"tipo": "formula", "formula": "\\frac{dv}{dt} + kv = g"})
        pasos.append({"tipo": "ok", "texto": "Ecuación LINEAL de primer orden (y también separable)"})
        pasos.append({"tipo": "titulo", "texto": "b) Solución general"})
        pasos.append({"tipo": "formula", "formula": "v(t) = \\frac{g}{k} + C\\,e^{-kt}"})
        pasos.append({"tipo": "titulo", "texto": "c) Velocidad límite (terminal)"})
        pasos.append({"tipo": "formula", "formula": "\\lim_{t \\to \\infty} v(t) = \\frac{g}{k}"})
        pasos.append({"tipo": "ok", "texto": "✔ v_límite = g/k  (ej: 9.8/0.2 = 49 m/s)"})

    return pasos

# ─────────────────────────────────────────────────────────────────
# RUTAS FLASK
# ─────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    import os
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'index.html')
    return render_template_string(open(template_path, encoding='utf-8').read())

@app.route('/api/lineal', methods=['POST'])
def api_lineal():
    try:
        d = request.json
        pasos = resolver_lineal(d['P'], d['Q'], d.get('var','x'),
                                d.get('x0'), d.get('y0'))
        return jsonify({"ok": True, "html": pasos_to_html(pasos)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/exacta', methods=['POST'])
def api_exacta():
    try:
        d = request.json
        pasos = resolver_exacta(d['M'], d['N'])
        return jsonify({"ok": True, "html": pasos_to_html(pasos)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/noexacta', methods=['POST'])
def api_noexacta():
    try:
        d = request.json
        pasos = resolver_no_exacta(d['M'], d['N'])
        return jsonify({"ok": True, "html": pasos_to_html(pasos)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/carbono14', methods=['POST'])
def api_carbono14():
    try:
        d = request.json
        pasos = resolver_carbono14(
            float(d.get('A0', 0) or 0),
            float(d.get('At', 0) or 0),
            float(d.get('t_med', 0) or 0),
            float(d.get('vida_media', 5730))
        )
        return jsonify({"ok": True, "html": pasos_to_html(pasos)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/ejercicio/<num>', methods=['GET'])
def api_ejercicio(num):
    try:
        pasos = resolver_ejercicio(num)
        return jsonify({"ok": True, "html": pasos_to_html(pasos)})
    except Exception as e:
        return jsonify({"ok": False, "error": traceback.format_exc()})

@app.route('/api/ejercicios', methods=['GET'])
def api_ejercicios():
    return jsonify(EJERCICIOS)

if __name__ == '__main__':
    app.run(debug=True, port=5000)