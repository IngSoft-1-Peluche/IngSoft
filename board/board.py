import numpy as np

TIPOS_CASILLAS = {
    "C": "Casilla común",
    "R": "Recinto",
    "M": "Murcielago",
    "S": "Serpiente",
    "E": "Escorpion",
    "A": "Araña",
    "T": "Trampa",
}

TRAMPAS = [22, 29, 56, 63]

COLORES = ["red", "green", "blue", "yellow", "deepskyblue", "orange"]

MATRIZ_TABLERO = np.genfromtxt("board/tablero.csv", delimiter=",")

MOVIMIENTOS = {
    1: np.genfromtxt("board/1mov.csv", delimiter=","),
    2: np.genfromtxt("board/2mov.csv", delimiter=","),
    3: np.genfromtxt("board/3mov.csv", delimiter=","),
    4: np.genfromtxt("board/4mov.csv", delimiter=","),
    5: np.genfromtxt("board/5mov.csv", delimiter=","),
    6: np.genfromtxt("board/6mov.csv", delimiter=","),
}

CASILLAS = {}

for i in range(1, 85):
    CASILLAS[i] = "C"

for i in [1, 3, 5, 36, 39, 70, 72, 74]:
    CASILLAS[i] = "R"

CASILLAS[12] = "M"
CASILLAS[11] = "E"
CASILLAS[19] = "S"
CASILLAS[30] = "S"
CASILLAS[54] = "A"
CASILLAS[65] = "A"
CASILLAS[71] = "M"
CASILLAS[73] = "E"

CASILLAS[22] = "T"
CASILLAS[29] = "T"
CASILLAS[56] = "T"
CASILLAS[63] = "T"


RECINTOS = {
    1: "Cochera",
    3: "Alcoba",
    5: "Biblioteca",
    36: "Vestibulo",
    39: "Panteon",
    70: "Bodega",
    72: "Salon",
    74: "Laboratorio",
}

PUERTAS = [2, 4, 16, 35, 50, 69, 83, 84]

CARTAS = [
    ("Alcoba", "R"),
    ("Biblioteca", "R"),
    ("Bodega", "R"),
    ("Cochera", "R"),
    ("Laboratorio", "R"),
    ("Panteon", "R"),
    ("Salon", "R"),
    ("Vestibulo", "R"),
    ("Bruja de Salem", "E"),
    ("Ama de llaves", "V"),
    ("Conde", "V"),
    ("Condesa", "V"),
    ("Doncella", "V"),
    ("Jardinero", "V"),
    ("Mayordomo", "V"),
    ("Dr. Jekyll Mr Hyde", "M"),
    ("Dracula", "M"),
    ("Fantasma", "M"),
    ("Frankenstein", "M"),
    ("Hombre lobo", "M"),
    ("Momia", "M"),
]
