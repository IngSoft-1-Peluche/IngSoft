import pony.orm as pony

from board.board import *


def posiciones_posibles_a_mover(posicion_inicial, numero_dado):
    posiciones_posibles = []
    matriz_movimientos = MOVIMIENTOS[numero_dado]
    if posicion_inicial in TRAMPAS:
        for posicion in TRAMPAS:
            for i in np.where(matriz_movimientos[:, posicion] > 0)[0]:
                posiciones_posibles.append(int(i))
    else:
        for i in np.where(matriz_movimientos[:, posicion_inicial] > 0)[0]:
            posiciones_posibles.append(int(i))
    return sorted(posiciones_posibles)
