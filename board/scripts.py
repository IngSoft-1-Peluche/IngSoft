import numpy as np
from board import CASILLAS

matriz_tablero = np.matrix(
    [
        [1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 6, 3, 3, 3, 3, 3, 3, 7, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 8, 3, 3, 3, 3, 3, 3, 9, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 10, 3, 3, 3, 3, 3, 3, 11, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 12, 3, 3, 3, 3, 3, 3, 13, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 14, 3, 3, 3, 3, 3, 3, 15, 5, 5, 5, 5, 5, 5],
        [
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
        ],
        [36, 36, 36, 36, 36, 36, 37, 0, 0, 0, 0, 0, 0, 38, 39, 39, 39, 39, 39, 39],
        [36, 36, 36, 36, 36, 36, 40, 0, 0, 0, 0, 0, 0, 41, 39, 39, 39, 39, 39, 39],
        [36, 36, 36, 36, 36, 36, 42, 0, 0, 0, 0, 0, 0, 43, 39, 39, 39, 39, 39, 39],
        [36, 36, 36, 36, 36, 36, 44, 0, 0, 0, 0, 0, 0, 45, 39, 39, 39, 39, 39, 39],
        [36, 36, 36, 36, 36, 36, 46, 0, 0, 0, 0, 0, 0, 47, 39, 39, 39, 39, 39, 39],
        [36, 36, 36, 36, 36, 36, 48, 0, 0, 0, 0, 0, 0, 49, 39, 39, 39, 39, 39, 39],
        [
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
        ],
        [
            70,
            70,
            70,
            70,
            70,
            70,
            71,
            72,
            72,
            72,
            72,
            72,
            72,
            73,
            74,
            74,
            74,
            74,
            74,
            74,
        ],
        [
            70,
            70,
            70,
            70,
            70,
            70,
            75,
            72,
            72,
            72,
            72,
            72,
            72,
            76,
            74,
            74,
            74,
            74,
            74,
            74,
        ],
        [
            70,
            70,
            70,
            70,
            70,
            70,
            77,
            72,
            72,
            72,
            72,
            72,
            72,
            78,
            74,
            74,
            74,
            74,
            74,
            74,
        ],
        [
            70,
            70,
            70,
            70,
            70,
            70,
            79,
            72,
            72,
            72,
            72,
            72,
            72,
            80,
            74,
            74,
            74,
            74,
            74,
            74,
        ],
        [
            70,
            70,
            70,
            70,
            70,
            70,
            81,
            72,
            72,
            72,
            72,
            72,
            72,
            82,
            74,
            74,
            74,
            74,
            74,
            74,
        ],
        [
            70,
            70,
            70,
            70,
            70,
            70,
            83,
            72,
            72,
            72,
            72,
            72,
            72,
            84,
            74,
            74,
            74,
            74,
            74,
            74,
        ],
    ]
)


def generar_aristas_movimiento():
    aristas_movimiento = [
        (1, 8),
        (20, 36),
        (53, 36),
        (44, 36),
        (70, 75),
        (72, 60),
        (74, 78),
        (39, 66),
        (39, 45),
        (39, 31),
        (5, 13),
        (3, 26),
    ]

    for i in range(1, 85):
        aristas_movimiento.append((i, i))

    for i in range(16, 35):
        aristas_movimiento.append((i, i + 1))

    for i in range(50, 69):
        aristas_movimiento.append((i, i + 1))

    for j in range(19):
        aristas_movimiento.append(
            (int(matriz_tablero[j, 6]), int(matriz_tablero[j + 1, 6]))
        )
        aristas_movimiento.append(
            (int(matriz_tablero[j, 13]), int(matriz_tablero[j + 1, 13]))
        )

    aranias = [k for k, v in CASILLAS.items() if v == "A"]
    escorpìones = [k for k, v in CASILLAS.items() if v == "E"]
    serpientes = [k for k, v in CASILLAS.items() if v == "S"]
    murcielagos = [k for k, v in CASILLAS.items() if v == "M"]
    aristas_movimiento.append((aranias[0], aranias[1]))
    aristas_movimiento.append((escorpìones[0], escorpìones[1]))
    aristas_movimiento.append((serpientes[0], serpientes[1]))
    aristas_movimiento.append((murcielagos[0], murcielagos[1]))

    return aristas_movimiento


aristas_movimiento = generar_aristas_movimiento()


def generar_matriz_adyacencia(aristas_movimiento):
    matriz = np.matrix(np.zeros((85, 85)))
    for i in range(85):
        for j in range(85):
            if (i, j) in aristas_movimiento or (j, i) in aristas_movimiento:
                matriz[i, j] = 1
    return matriz


matriz_adyacencia = generar_matriz_adyacencia(aristas_movimiento)

np.savetxt("board/tablero.csv", matriz_tablero, fmt="%i", delimiter=",")

mov_1 = matriz_adyacencia
mov_2 = matriz_adyacencia ** 2
mov_3 = matriz_adyacencia ** 3
mov_4 = matriz_adyacencia ** 4
mov_5 = matriz_adyacencia ** 5
mov_6 = matriz_adyacencia ** 6

np.savetxt("board/1mov.csv", mov_1, fmt="%i", delimiter=",")
np.savetxt("board/2mov.csv", mov_2, fmt="%i", delimiter=",")
np.savetxt("board/3mov.csv", mov_3, fmt="%i", delimiter=",")
np.savetxt("board/4mov.csv", mov_4, fmt="%i", delimiter=",")
np.savetxt("board/5mov.csv", mov_5, fmt="%i", delimiter=",")
np.savetxt("board/6mov.csv", mov_6, fmt="%i", delimiter=",")
