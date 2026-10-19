"""
Entorno simulado: Sistema Inteligente de Gestión de la Movilidad (SIGA).
Sistemas Inteligentes

El entorno representa el tráfico vehicular en Cocula, Jalisco.
El agente percibe el tráfico, la velocidad y la cantidad de vehículos.
Decide cómo ajustar los semáforos para mejorar la circulación.
"""

class SIGA:
    """Entorno: tráfico vehicular en Cocula, Jalisco."""


def percibe(trafico, velocidad, vehiculos):
    # Percibe los datos del tráfico
    return trafico, velocidad, vehiculos


def decide(datos):
    # Decide cómo ajustar los semáforos
    agente = AgenteReactivo()
    return agente.actuar(datos)


def acciona(ajuste):
    # Representa la acción sobre los semáforos
    return "Acción realizada: " + ajuste


class AgenteReactivo:
    """Agente reactivo simple.

    Regla: la acción depende únicamente de la percepción actual.
    No guarda información entre pasos.

    percepción (tuple):
        trafico     nivel de tráfico (alto, medio o bajo)
        velocidad   velocidad de los vehículos en km/h
        vehiculos   cantidad de vehículos
    """

    def actuar(self, datos):
        trafico, velocidad, vehiculos = datos
        trafico = trafico.lower()
        velocidad = float(velocidad)
        vehiculos = int(vehiculos)

        if trafico == "alto" or vehiculos >= 30:
            return "dar más tiempo al semáforo en verde"
        elif trafico == "medio" or vehiculos >= 15 or velocidad < 40:
            return "ajustar los tiempos de los semáforos"
        else:
            return "mantener los tiempos de los semáforos"


trafico = input("Ingresa el tráfico (alto, medio o bajo): ")
velocidad = input("Ingresa la velocidad en km/h: ")
vehiculos = input("Ingresa la cantidad de vehículos: ")

datos = percibe(trafico, velocidad, vehiculos)
ajuste = decide(datos)
resultado = acciona(ajuste)

print("Datos:", datos)
print("Decisión:", ajuste)
print("Resultado:", resultado)
