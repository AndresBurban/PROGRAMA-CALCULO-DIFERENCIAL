from flask import jsonify

from models.ejercicios_model import (
    obtener_ejercicio,
    obtener_todos,
    existe_ejercicio,
    cantidad_ejercicios
)


def resolver_ejercicio_controller(num):

    try:

        if not existe_ejercicio(num):

            return jsonify({

                "ok": False,

                "mensaje": "El ejercicio no existe."

            }), 404

        ejercicio = obtener_ejercicio(num)

        return jsonify({

            "ok": True,

            "ejercicio": ejercicio

        })

    except Exception as e:

        return jsonify({

            "ok": False,

            "error": str(e)

        }), 500


def listar_ejercicios_controller():

    try:

        ejercicios = obtener_todos()

        return jsonify({

            "ok": True,

            "cantidad": cantidad_ejercicios(),

            "ejercicios": ejercicios

        })

    except Exception as e:

        return jsonify({

            "ok": False,

            "error": str(e)

        }), 500