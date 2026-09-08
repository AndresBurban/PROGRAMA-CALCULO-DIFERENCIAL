from flask import request
from flask import jsonify

from models.no_exacta_model import resolver_no_exacta
from models.helpers import pasos_to_html


def resolver_no_exacta_controller():

    try:

        datos = request.get_json(silent=True) or {}

        if not datos.get("M") or not datos.get("N"):
            raise ValueError("M y N son obligatorios.")

        M = datos["M"]

        N = datos["N"]

        pasos = resolver_no_exacta(

            M,

            N

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