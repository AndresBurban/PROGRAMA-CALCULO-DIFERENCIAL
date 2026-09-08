from flask import request
from flask import jsonify

from models.carbono_model import resolver_carbono
from models.helpers import pasos_to_html


def resolver_carbono_controller():

    try:

        datos = request.get_json(silent=True) or {}

        if any(datos.get(campo) in (None, "") for campo in (
            "vida_media", "cantidad_inicial", "cantidad_final"
        )):
            raise ValueError("Todos los valores de Carbono-14 son obligatorios.")

        vida_media = float(datos["vida_media"])

        cantidad_inicial = float(datos["cantidad_inicial"])

        cantidad_final = float(datos["cantidad_final"])

        pasos = resolver_carbono(

            vida_media,

            cantidad_inicial,

            cantidad_final

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