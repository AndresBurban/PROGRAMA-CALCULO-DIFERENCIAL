from flask import jsonify, request

from models.helpers import pasos_to_html
from models.separable_model import resolver_separable


def resolver_separable_controller():
    try:
        datos = request.get_json(silent=True) or {}

        if any(datos.get(campo) in (None, "") for campo in ("f", "g")):
            raise ValueError("f(x) y g(y) son obligatorias.")

        x0 = datos.get("x0")
        y0 = datos.get("y0")

        pasos = resolver_separable(
            datos["f"],
            datos["g"],
            x0 if x0 not in (None, "") else None,
            y0 if y0 not in (None, "") else None
        )

        return jsonify({"ok": True, "html": pasos_to_html(pasos)})
    except Exception as error:
        return jsonify({"ok": False, "error": str(error)}), 400