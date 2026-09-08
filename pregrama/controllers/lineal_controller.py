from flask import request
from flask import jsonify

from models.lineal_model import resolver_lineal
from models.helpers import pasos_to_html


def resolver_lineal_controller():

    try:

        datos = request.get_json(silent=True) or {}

        if not datos.get("P") or not datos.get("Q"):
            raise ValueError("P y Q son obligatorios.")

        if (datos.get("x0") == "") != (datos.get("y0") == ""):
            raise ValueError("Debes indicar x0 y y0 juntos.")

        P = datos["P"]

        Q = datos["Q"]

        variable = datos.get("var", "x")

        x0 = datos.get("x0")

        y0 = datos.get("y0")

        pasos = resolver_lineal(

            P,

            Q,

            variable,

            x0,

            y0

        )

        html = pasos_to_html(pasos)

        return jsonify({

            "ok": True,

            "html": html

        })

    except Exception as e:

        return jsonify({

            "ok": False,

            "error": str(e)

        }), 400