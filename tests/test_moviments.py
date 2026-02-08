import copy
import escacs_prog
import pytest

TAULER_INICIAL = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

@pytest.fixture(autouse=True)
def reset_tauler():
    escacs_prog.tauler = copy.deepcopy(TAULER_INICIAL)

def test_peon_blanco_avanza_una():
    assert escacs_prog.movimiento_valido(6, 0, 5, 0, True)

def test_peon_blanco_doble_inicial():
    assert escacs_prog.movimiento_valido(6, 1, 4, 1, True)

def test_peon_blanco_no_doble_si_no_inicial():
    escacs_prog.tauler[5][0] = "P"
    escacs_prog.tauler[6][0] = " "
    assert not escacs_prog.movimiento_valido(5, 0, 3, 0, True)

def test_peon_negro_avanza_una():
    assert escacs_prog.movimiento_valido(1, 0, 2, 0, False)

def test_peon_captura_diagonal():
    escacs_prog.tauler[5][1] = "p"
    assert escacs_prog.movimiento_valido(6, 0, 5, 1, True)

def test_peon_no_avanza_si_ocupado():
    escacs_prog.tauler[5][0] = "p"
    assert not escacs_prog.movimiento_valido(6, 0, 5, 0, True)

def test_caballo_movimiento_L_1():
    assert escacs_prog.movimiento_valido(7, 1, 5, 2, True)

def test_caballo_movimiento_L_2():
    assert escacs_prog.movimiento_valido(7, 6, 5, 5, True)

def test_caballo_salta_piezas():
    escacs_prog.tauler[6][2] = "p"
    assert escacs_prog.movimiento_valido(7, 1, 5, 2, True)

def test_caballo_movimiento_invalido():
    assert not escacs_prog.movimiento_valido(7, 1, 6, 1, True)

def test_caballo_fuera_tablero():
    assert not escacs_prog.movimiento_valido(7, 1, 9, 2, True)

def test_caballo_no_en_su_turno():
    assert not escacs_prog.movimiento_valido(7, 1, 5, 2, False)
