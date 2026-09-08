from data.ejercicios import EJERCICIOS


def obtener_ejercicio(numero):
    """
    Retorna un ejercicio según su número.
    """

    numero = int(numero)

    if numero not in EJERCICIOS:

        return None

    return EJERCICIOS[numero]


def obtener_todos():
    """
    Retorna todos los ejercicios.
    """

    return EJERCICIOS


def existe_ejercicio(numero):
    """
    Verifica si un ejercicio existe.
    """

    return int(numero) in EJERCICIOS


def cantidad_ejercicios():
    """
    Retorna la cantidad de ejercicios.
    """

    return len(EJERCICIOS)