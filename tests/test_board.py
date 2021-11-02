from services.board_functions import posiciones_posibles_a_mover

def test_posiciones_posibles_a_mover():
    assert posiciones_posibles_a_mover(83, 1) == [81]
    assert posiciones_posibles_a_mover(69, 2) == [67, 69]
    assert posiciones_posibles_a_mover(58, 3) == [48, 55, 57, 59, 61, 71, 72]