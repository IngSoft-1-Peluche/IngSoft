import numpy as np

TIPOS_CASILLAS = {
    "C": "Casilla común",
    "R": "Recinto"
}

MATRIZ_TABLERO = np.genfromtxt('board/tablero.csv', delimiter=',')

MOVIMIENTOS = {
    1: np.genfromtxt('board/1mov.csv', delimiter=','),
    2: np.genfromtxt('board/2mov.csv', delimiter=','),
    3: np.genfromtxt('board/3mov.csv', delimiter=','),
    4: np.genfromtxt('board/4mov.csv', delimiter=','),
    5: np.genfromtxt('board/5mov.csv', delimiter=','),
    6: np.genfromtxt('board/6mov.csv', delimiter=',')
}

CASILLAS = {}

for i in range(1,85):
    CASILLAS[i] = "C"

for i in [1,3,5,36,39,70,72,74]:
    CASILLAS[i] = "R"
