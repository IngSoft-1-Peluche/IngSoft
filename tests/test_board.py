from services.board_functions import posiciones_posibles_a_mover


def test_posiciones_posibles_a_mover():
    assert posiciones_posibles_a_mover(83, 1) == [81, 83]
    assert posiciones_posibles_a_mover(69, 2) == [67, 68, 69]
    assert posiciones_posibles_a_mover(58, 3) == [48, 55, 56, 57, 58, 59, 60, 61, 71, 72]


def test_posiciones_posibles_a_mover_casilla_especial():
    assert posiciones_posibles_a_mover(10, 2) == [1, 6, 8, 10, 12, 14, 71]
    assert posiciones_posibles_a_mover(54, 1) == [53, 54, 55, 65]