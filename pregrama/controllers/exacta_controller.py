from flask import request
from flask import jsonify

from models.exacta_model import resolver_exacta
from models.helpers import pasos_to_html


def resolver_exacta_controller():

    try:

        datos = request.get_json(silent=True) or {}

        if not datos.get("M") or not datos.get("N"):
            raise ValueError("M y N son obligatorios.")

        M = datos["M"]

        N = datos["N"]

        variable = datos.get("var", "x")

        pasos = resolver_exacta(

            M,

            N,

            variable

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