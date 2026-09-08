from flask import Blueprint

from controllers.lineal_controller import resolver_lineal_controller
from controllers.exacta_controller import resolver_exacta_controller
from controllers.no_exacta_controller import resolver_no_exacta_controller
from controllers.carbono_controller import resolver_carbono_controller
from controllers.separable_controller import resolver_separable_controller
from controllers.ejercicios_controller import (
    resolver_ejercicio_controller,
    listar_ejercicios_controller
)


api = Blueprint("api", __name__)


# ===========================
# ECUACIÓN LINEAL
# ===========================

api.route(
    "/lineal",
    methods=["POST"]
)(resolver_lineal_controller)


# ===========================
# ECUACIÓN EXACTA
# ===========================

api.route(
    "/exacta",
    methods=["POST"]
)(resolver_exacta_controller)


# ===========================
# ECUACIÓN NO EXACTA
# ===========================

api.route(
    "/noexacta",
    methods=["POST"]
)(resolver_no_exacta_controller)


# ===========================
# CARBONO 14
# ===========================

api.route(
    "/carbono14",
    methods=["POST"]
)(resolver_carbono_controller)


# ===========================
# ECUACION DE VARIABLES SEPARABLES
# ===========================

api.route(
    "/separable",
    methods=["POST"]
)(resolver_separable_controller)


# ===========================
# EJERCICIOS
# ===========================

api.route(
    "/ejercicio/<num>",
    methods=["GET"]
)(resolver_ejercicio_controller)

api.route(
    "/ejercicios",
    methods=["GET"]
)(listar_ejercicios_controller)