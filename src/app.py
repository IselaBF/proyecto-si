"""
Entorno simulado: Sistema Inteligente de Gestión de la Movilidad (SIGA).
Sistemas Inteligentes

El entorno representa el tráfico vehicular en Cocula, Jalisco.
El agente percibe el tráfico, la velocidad y la cantidad de vehículos.
Decide cómo ajustar los semáforos para mejorar la circulación.
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (9, 3.2)
plt.rcParams["axes.grid"] = True


# Funciones de membresía 
def triangular(x, a, b, c):
    """Grado de membresia triangular. Debe admitir a == b o b == c."""
    x = np.asarray(x, dtype=float)

    sube = np.ones_like(x) if a == b else (x - a) / (b - a)
    baja = np.ones_like(x) if b == c else (c - x) / (c - b)

    miu = np.clip(np.minimum(sube, baja), 0.0, 1.0)
    return np.where((x < a) | (x > c), 0.0, miu)


def trapezoidal(x, a, b, c, d):
    """Grado de membresia trapezoidal. Debe admitir a == b o c == d."""
    x = np.asarray(x, dtype=float)

    sube = np.ones_like(x) if a == b else (x - a) / (b - a)
    baja = np.ones_like(x) if c == d else (d - x) / (d - c)
    miu = np.clip(np.minimum(np.minimum(sube, 1.0), baja), 0.0, 1.0)
    return np.where((x < a) | (x > d), 0.0, miu)


def gaussiana(x, media, sigma):
    """Grado de membresia gaussiano."""
    x = np.asarray(x, dtype=float)

    miu = np.exp(-((x - media) ** 2) / (2 * sigma ** 2))

    return np.clip(miu, 0.0, 1.0)


def graficar_variable(nombre, universo, conjuntos, marcar=None):
    """conjuntos: diccionario {nombre: arreglo de membresia}."""
    fig, ax = plt.subplots()
    for etiqueta, mu in conjuntos.items():
        ax.plot(universo, mu, linewidth=2.5, label=etiqueta)
        ax.fill_between(universo, mu, alpha=0.08)
    if marcar is not None:
        ax.axvline(marcar, linestyle="--", color="gray")
    ax.set_ylim(-0.03, 1.08)
    ax.set_xlabel(nombre)
    ax.set_ylabel("grado de membresia")
    ax.legend(loc="center right")
    plt.show()


# Grados de membresía de un valor
def grados(valor, universo, conjuntos):
    """Devuelve {conjunto: grado de membresía} para un valor dado."""
    return {etiqueta: float(np.interp(valor, universo, mu))
            for etiqueta, mu in conjuntos.items()}


def imprimir_grados(nombre, valor, universo, conjuntos):
    print(f"\n{nombre} = {valor}")
    resultado = grados(valor, universo, conjuntos)
    for etiqueta, g in resultado.items():
        print(f"   {etiqueta:<10} -> {g:.2f}")
    dominante = max(resultado, key=resultado.get)
    print(f"   Conjunto dominante: {dominante}")


# Entorno y agente SIGA
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


# Variables difusas del contexto (tráfico en Cocula)
# Vehículos (0 a 60)
x_veh = np.linspace(0, 60, 601)
vehiculos_mf = {
    "pocos":     trapezoidal(x_veh, 0, 0, 10, 20),
    "moderados": triangular(x_veh, 15, 25, 35),
    "muchos":    trapezoidal(x_veh, 30, 40, 60, 60),
}

# Velocidad en km/h (0 a 80)
x_vel = np.linspace(0, 80, 801)
velocidad_mf = {
    "lenta":    trapezoidal(x_vel, 0, 0, 20, 40),
    "moderada": triangular(x_vel, 30, 50, 70),
    "rápida":   trapezoidal(x_vel, 60, 70, 80, 80),
}

# Nivel de tráfico (escala 0 a 10: bajo ≈ 1, medio ≈ 5, alto ≈ 9)
x_traf = np.linspace(0, 10, 1001)
trafico_mf = {
    "bajo":  trapezoidal(x_traf, 0, 0, 2, 4),
    "medio": triangular(x_traf, 3, 5, 7),
    "alto":  trapezoidal(x_traf, 6, 8, 10, 10),
}
NIVEL_TRAFICO = {"bajo": 1, "medio": 5, "alto": 9}


# Ejecución
trafico = input("Ingresa el tráfico (alto, medio o bajo): ")
velocidad = input("Ingresa la velocidad en km/h: ")
vehiculos = input("Ingresa la cantidad de vehículos: ")

datos = percibe(trafico, velocidad, vehiculos)
ajuste = decide(datos)
resultado = acciona(ajuste)

print("\n=== Resultados del agente ===")
print("Datos:", datos)
print("Decisión:", ajuste)
print("Resultado:", resultado)

veh = int(vehiculos)
vel = float(velocidad)
traf = NIVEL_TRAFICO.get(trafico.lower())

print("\n=== Grados de membresía ===")
imprimir_grados("Vehículos", veh, x_veh, vehiculos_mf)
imprimir_grados("Velocidad (km/h)", vel, x_vel, velocidad_mf)
if traf is not None:
    imprimir_grados("Nivel de tráfico", traf, x_traf, trafico_mf)

# Gráficas con el valor ingresado marcado
graficar_variable("Cantidad de vehículos", x_veh, vehiculos_mf, marcar=veh)
graficar_variable("Velocidad (km/h)", x_vel, velocidad_mf, marcar=vel)
graficar_variable("Nivel de tráfico (1 = bajo, 5 = medio, 9 = alto)",
                  x_traf, trafico_mf, marcar=traf)
