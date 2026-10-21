import pytest

from src.systems.pontuacao import MAXIMO_FASE, MAXIMO_TOTAL, PlacarFases, pontos_da_fase


@pytest.mark.parametrize("acertos,esperado", [(0, 0), (1, 100), (4, 400), (5, 550)])
def test_pontos_da_fase(acertos, esperado):
    assert pontos_da_fase(acertos) == esperado


@pytest.mark.parametrize("ruim", [-1, 6, 2.5, "3", True, None])
def test_acertos_invalidos(ruim):
    with pytest.raises(ValueError):
        pontos_da_fase(ruim)


def test_maximos():
    assert MAXIMO_FASE == 550 and MAXIMO_TOTAL == 1650


def test_melhor_pontuacao_nao_acumula():
    p = PlacarFases()
    assert p.registrar(1, 3) is True and p.melhor(1) == 300
    assert p.registrar(1, 2) is False and p.melhor(1) == 300     # pior: não substitui
    assert p.registrar(1, 3) is False and p.total == 300         # igual: não soma de novo
    assert p.registrar(1, 5) is True and p.total == 550          # melhor: substitui, não soma


def test_total_maximo():
    p = PlacarFases()
    for f in (1, 2, 3):
        p.registrar(f, 5)
    assert p.total == 1650


def test_liberacao_exige_tres_acertos():
    p = PlacarFases()
    assert p.liberada(1) and not p.liberada(2)
    p.registrar(1, 2)                      # concluiu, mas com 2 acertos: não passa
    assert p.concluida(1) and not p.aprovada(1) and not p.liberada(2)
    p.registrar(1, 3)
    assert p.aprovada(1) and p.liberada(2) and not p.liberada(3)


def test_fase_invalida_e_placar_invalido():
    with pytest.raises(ValueError):
        PlacarFases().registrar(4, 3)
    with pytest.raises(ValueError):
        PlacarFases(melhores=[0, 0, 999])
