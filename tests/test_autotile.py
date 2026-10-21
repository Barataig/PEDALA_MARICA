import itertools

from src.world.autotile import escolher_celula


def test_16_combinacoes_usam_16_pecas_diferentes():
    pecas = {escolher_celula(*c) for c in itertools.product([0, 1], repeat=4)}
    assert len(pecas) == 16 and pecas == {(c, l) for c in range(4) for l in range(4)}


def test_casos_principais():
    assert escolher_celula(1, 1, 1, 1) == (1, 1)    # miolo
    assert escolher_celula(0, 1, 1, 0) == (0, 0)    # canto superior esquerdo
    assert escolher_celula(1, 0, 0, 1) == (2, 2)    # canto inferior direito
    assert escolher_celula(0, 0, 0, 0) == (3, 3)    # isolado
