"""Escolhe a peça do terreno (folha 4x4 do Tiny Swords) pelos 4 vizinhos."""

# (norte, leste, sul, oeste) com terreno igual -> (coluna, linha) na folha
_TABELA = {
    (1, 1, 1, 1): (1, 1),
    (0, 1, 1, 1): (1, 0), (1, 1, 0, 1): (1, 2),
    (1, 1, 1, 0): (0, 1), (1, 0, 1, 1): (2, 1),
    (0, 1, 1, 0): (0, 0), (0, 0, 1, 1): (2, 0),
    (1, 1, 0, 0): (0, 2), (1, 0, 0, 1): (2, 2),
    (1, 0, 1, 0): (3, 1), (0, 0, 1, 0): (3, 0), (1, 0, 0, 0): (3, 2),
    (0, 1, 0, 1): (1, 3), (0, 1, 0, 0): (0, 3), (0, 0, 0, 1): (2, 3),
    (0, 0, 0, 0): (3, 3),
}


def escolher_celula(norte, leste, sul, oeste):
    return _TABELA[(int(norte), int(leste), int(sul), int(oeste))]
